from sqlalchemy.orm import Session
from models.cart import Cart, CartItem
from models.product import ProductVariant
from schemas.cart import CartCreate, CartItemCreate, CartItemUpdate
from typing import List, Optional, Dict, Any
import uuid
import logging

logger = logging.getLogger(__name__)

class CartService:
    
    def create_cart(self, db: Session, cart_data: CartCreate) -> Dict[str, Any]:
        """새 장바구니 생성"""
        cart = Cart(
            user_id=cart_data.user_id,
            session_id=str(uuid.uuid4())
        )
        
        db.add(cart)
        db.commit()
        db.refresh(cart)
        
        return cart.to_dict()
    
    def get_cart(self, db: Session, cart_id: str) -> Optional[Dict[str, Any]]:
        """장바구니 조회"""
        try:
            cart = db.query(Cart).filter(Cart.id == cart_id).first()
            if not cart:
                return None
            
            # 안전하게 to_dict 호출
            return cart.to_dict()
        except Exception as e:
            logger.error(f"Error in get_cart: {e}")
            # 기본 cart 정보만 반환
            if cart:
                return {
                    'id': cart.id,
                    'user_id': cart.user_id,
                    'session_id': cart.session_id,
                    'currency_code': cart.currency_code,
                    'created_at': cart.created_at.isoformat() if cart.created_at else None,
                    'updated_at': cart.updated_at.isoformat() if cart.updated_at else None,
                    'items': [],
                    'total_quantity': 0,
                    'cost': {
                        'subtotal_amount': {'amount': '0.00', 'currency_code': cart.currency_code},
                        'total_amount': {'amount': '0.00', 'currency_code': cart.currency_code},
                        'total_tax_amount': {'amount': '0.00', 'currency_code': cart.currency_code}
                    }
                }
            return None
    
    def add_items_to_cart(
        self, 
        db: Session, 
        cart_id: str, 
        items: List[CartItemCreate]
    ) -> Optional[Dict[str, Any]]:
        """장바구니에 상품 추가"""
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            return None
        
        for item_data in items:
            # 변형 상품 존재 확인
            variant = db.query(ProductVariant).filter(
                ProductVariant.id == item_data.variant_id
            ).first()
            
            if not variant:
                raise ValueError(f"Product variant {item_data.variant_id} not found")
            
            if not variant.available_for_sale:
                raise ValueError(f"Product variant {item_data.variant_id} is not available for sale")
            
            # 재고 확인
            if variant.inventory_quantity < item_data.quantity:
                raise ValueError(f"Insufficient inventory for variant {item_data.variant_id}")
            
            # 기존 장바구니 아이템 확인
            existing_item = db.query(CartItem).filter(
                CartItem.cart_id == cart_id,
                CartItem.variant_id == item_data.variant_id
            ).first()
            
            if existing_item:
                # 기존 아이템의 수량 업데이트
                new_quantity = existing_item.quantity + item_data.quantity
                
                # 재고 재확인
                if variant.inventory_quantity < new_quantity:
                    raise ValueError(f"Insufficient inventory for variant {item_data.variant_id}")
                
                existing_item.quantity = new_quantity
            else:
                # 새 아이템 추가
                cart_item = CartItem(
                    cart_id=cart_id,
                    variant_id=item_data.variant_id,
                    quantity=item_data.quantity
                )
                db.add(cart_item)
        
        db.commit()
        db.refresh(cart)
        
        return cart.to_dict()
    
    def update_cart_items(
        self, 
        db: Session, 
        cart_id: str, 
        items: List[CartItemUpdate]
    ) -> Optional[Dict[str, Any]]:
        """장바구니 상품 수량 업데이트"""
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            return None
        
        for item_data in items:
            cart_item = db.query(CartItem).filter(
                CartItem.id == item_data.id,
                CartItem.cart_id == cart_id
            ).first()
            
            if not cart_item:
                raise ValueError(f"Cart item {item_data.id} not found")
            
            if item_data.quantity <= 0:
                # 수량이 0 이하면 아이템 삭제
                db.delete(cart_item)
            else:
                # 재고 확인
                variant = cart_item.variant
                if variant and variant.inventory_quantity < item_data.quantity:
                    raise ValueError(f"Insufficient inventory for variant {cart_item.variant_id}")
                
                # 수량 업데이트
                cart_item.quantity = item_data.quantity
                
                # 변형 상품 변경 (선택사항)
                if item_data.variant_id and item_data.variant_id != cart_item.variant_id:
                    new_variant = db.query(ProductVariant).filter(
                        ProductVariant.id == item_data.variant_id
                    ).first()
                    
                    if not new_variant:
                        raise ValueError(f"Product variant {item_data.variant_id} not found")
                    
                    if not new_variant.available_for_sale:
                        raise ValueError(f"Product variant {item_data.variant_id} is not available for sale")
                    
                    if new_variant.inventory_quantity < item_data.quantity:
                        raise ValueError(f"Insufficient inventory for variant {item_data.variant_id}")
                    
                    cart_item.variant_id = item_data.variant_id
        
        db.commit()
        db.refresh(cart)
        
        return cart.to_dict()
    
    def remove_items_from_cart(
        self, 
        db: Session, 
        cart_id: str, 
        item_ids: List[int]
    ) -> bool:
        """장바구니에서 상품 제거"""
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            return False
        
        # 아이템들 삭제
        deleted_count = 0
        for item_id in item_ids:
            cart_item = db.query(CartItem).filter(
                CartItem.id == item_id,
                CartItem.cart_id == cart_id
            ).first()
            
            if cart_item:
                db.delete(cart_item)
                deleted_count += 1
        
        if deleted_count == 0:
            return False
        
        db.commit()
        return True
    
    def clear_cart(self, db: Session, cart_id: str) -> bool:
        """장바구니 비우기"""
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            return False
        
        # 모든 아이템 삭제
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        db.commit()
        
        return True
    
    def delete_cart(self, db: Session, cart_id: str) -> bool:
        """장바구니 삭제"""
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            return False
        
        db.delete(cart)
        db.commit()
        
        return True
    
    def get_cart_by_session(self, db: Session, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 ID로 장바구니 조회"""
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
        return cart.to_dict() if cart else None
