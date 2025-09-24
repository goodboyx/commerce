from sqlalchemy.orm import Session
from models.order import Order, OrderItem, OrderStatus, PaymentStatus
from models.cart import Cart, CartItem
from models.product import ProductVariant
from typing import Dict, Any, Optional, List
import uuid
import datetime

class OrderService:
    
    def create_order_from_cart(
        self, 
        db: Session, 
        cart_id: str,
        email: str,
        shipping_address: str,
        billing_address: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """장바구니에서 주문 생성"""
        
        # 장바구니 조회
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            raise ValueError("Cart not found")
        
        if not cart.items:
            raise ValueError("Cart is empty")
        
        # 재고 확인
        for cart_item in cart.items:
            variant = cart_item.variant
            if not variant:
                raise ValueError(f"Product variant not found for cart item {cart_item.id}")
            
            if not variant.available_for_sale:
                raise ValueError(f"Product variant {variant.id} is not available for sale")
            
            if variant.inventory_quantity < cart_item.quantity:
                raise ValueError(f"Insufficient inventory for product {variant.title}")
        
        # 주문 번호 생성
        order_number = self._generate_order_number()
        
        # 금액 계산
        subtotal_amount = cart.subtotal_amount
        tax_amount = self._calculate_tax(subtotal_amount)
        shipping_amount = self._calculate_shipping(subtotal_amount)
        total_amount = subtotal_amount + tax_amount + shipping_amount
        
        # 주문 생성
        order = Order(
            order_number=order_number,
            user_id=cart.user_id,
            email=email,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            subtotal_amount=subtotal_amount,
            tax_amount=tax_amount,
            shipping_amount=shipping_amount,
            total_amount=total_amount,
            currency_code=cart.currency_code,
            shipping_address=shipping_address,
            billing_address=billing_address or shipping_address,
            notes=notes
        )
        
        db.add(order)
        db.flush()  # ID 생성을 위해
        
        # 주문 아이템 생성
        for cart_item in cart.items:
            variant = cart_item.variant
            
            order_item = OrderItem(
                order_id=order.id,
                variant_id=variant.id,
                quantity=cart_item.quantity,
                price=variant.price,
                total_amount=float(variant.price) * cart_item.quantity,
                product_title=variant.product.title if variant.product else None,
                variant_title=variant.title,
                product_handle=variant.product.handle if variant.product else None
            )
            
            db.add(order_item)
            
            # 재고 차감
            variant.inventory_quantity -= cart_item.quantity
        
        # 장바구니 비우기
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        
        db.commit()
        db.refresh(order)
        
        return order.to_dict()
    
    def get_order(self, db: Session, order_id: str) -> Optional[Dict[str, Any]]:
        """주문 조회"""
        order = db.query(Order).filter(Order.id == order_id).first()
        return order.to_dict() if order else None
    
    def get_order_by_number(self, db: Session, order_number: str) -> Optional[Dict[str, Any]]:
        """주문 번호로 주문 조회"""
        order = db.query(Order).filter(Order.order_number == order_number).first()
        return order.to_dict() if order else None
    
    def get_user_orders(
        self, 
        db: Session, 
        user_id: str,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """사용자 주문 목록 조회"""
        
        query = db.query(Order).filter(Order.user_id == user_id)
        
        # 총 개수 계산
        total = query.count()
        
        # 페이지네이션 적용
        offset = (page - 1) * per_page
        orders = query.order_by(Order.created_at.desc()).offset(offset).limit(per_page).all()
        
        # 총 페이지 수 계산
        import math
        pages = math.ceil(total / per_page)
        
        return {
            "orders": [order.to_dict() for order in orders],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages
        }
    
    def update_order_status(
        self, 
        db: Session, 
        order_id: str, 
        status: OrderStatus
    ) -> Optional[Dict[str, Any]]:
        """주문 상태 업데이트"""
        
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        order.status = status
        
        # 상태에 따른 타임스탬프 업데이트
        if status == OrderStatus.SHIPPED:
            order.shipped_at = datetime.datetime.utcnow()
        elif status == OrderStatus.DELIVERED:
            order.delivered_at = datetime.datetime.utcnow()
        
        db.commit()
        db.refresh(order)
        
        return order.to_dict()
    
    def update_payment_status(
        self, 
        db: Session, 
        order_id: str, 
        payment_status: PaymentStatus,
        payment_id: Optional[str] = None,
        payment_method: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """결제 상태 업데이트"""
        
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        order.payment_status = payment_status
        
        if payment_id:
            order.payment_id = payment_id
        
        if payment_method:
            order.payment_method = payment_method
        
        # 결제 완료 시 주문 상태도 업데이트
        if payment_status == PaymentStatus.PAID and order.status == OrderStatus.PENDING:
            order.status = OrderStatus.CONFIRMED
        
        db.commit()
        db.refresh(order)
        
        return order.to_dict()
    
    def cancel_order(self, db: Session, order_id: str) -> Optional[Dict[str, Any]]:
        """주문 취소"""
        
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        # 취소 가능한 상태인지 확인
        if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise ValueError("Cannot cancel shipped or delivered order")
        
        # 재고 복원
        for order_item in order.items:
            variant = order_item.variant
            if variant:
                variant.inventory_quantity += order_item.quantity
        
        # 주문 상태 업데이트
        order.status = OrderStatus.CANCELLED
        
        db.commit()
        db.refresh(order)
        
        return order.to_dict()
    
    def _generate_order_number(self) -> str:
        """주문 번호 생성"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        random_part = str(uuid.uuid4()).replace("-", "")[:8].upper()
        return f"ORD-{timestamp}-{random_part}"
    
    def _calculate_tax(self, subtotal: float) -> float:
        """세금 계산 (예시: 10%)"""
        return round(subtotal * 0.1, 2)
    
    def _calculate_shipping(self, subtotal: float) -> float:
        """배송비 계산"""
        # 예시: $50 이상 무료배송
        if subtotal >= 50:
            return 0.0
        return 5.99
