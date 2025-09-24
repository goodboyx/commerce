from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import uuid
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number = Column(String(50), unique=True, index=True)
    user_id = Column(String(36), nullable=True)
    email = Column(String(255), nullable=False)
    
    # 주문 상태
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # 금액 정보
    subtotal_amount = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), default=0)
    shipping_amount = Column(DECIMAL(10, 2), default=0)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    currency_code = Column(String(3), default="USD")
    
    # 결제 정보
    payment_id = Column(String(255))
    payment_method = Column(String(50))
    
    # 배송 정보
    shipping_address = Column(Text)
    billing_address = Column(Text)
    
    # 메모
    notes = Column(Text)
    
    # 타임스탬프
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    
    # 관계
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'email': self.email,
            'status': self.status.value if self.status else None,
            'payment_status': self.payment_status.value if self.payment_status else None,
            'subtotal_amount': float(self.subtotal_amount) if self.subtotal_amount else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0,
            'shipping_amount': float(self.shipping_amount) if self.shipping_amount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'currency_code': self.currency_code,
            'payment_id': self.payment_id,
            'payment_method': self.payment_method,
            'shipping_address': self.shipping_address,
            'billing_address': self.billing_address,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)  # 주문 시점의 가격 저장
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    
    # 제품 정보 스냅샷 (주문 시점의 정보 보존)
    product_title = Column(String(500))
    variant_title = Column(String(255))
    product_handle = Column(String(255))
    
    created_at = Column(DateTime, server_default=func.now())
    
    # 관계
    order = relationship("Order", back_populates="items")
    variant = relationship("ProductVariant")
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'variant_id': self.variant_id,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'product_title': self.product_title,
            'variant_title': self.variant_title,
            'product_handle': self.product_handle,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'variant': self.variant.to_dict() if self.variant else None
        }
