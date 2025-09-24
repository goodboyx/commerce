from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)  # 게스트 카트 지원
    session_id = Column(String(255), index=True)
    currency_code = Column(String(3), default="USD")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    
    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items)
    
    @property
    def subtotal_amount(self):
        return sum(item.total_amount for item in self.items)
    
    @property
    def total_amount(self):
        # 세금 계산 로직 추가 가능
        return self.subtotal_amount
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'currency_code': self.currency_code,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items],
            'total_quantity': self.total_quantity,
            'cost': {
                'subtotal_amount': {
                    'amount': str(self.subtotal_amount),
                    'currency_code': self.currency_code
                },
                'total_amount': {
                    'amount': str(self.total_amount),
                    'currency_code': self.currency_code
                },
                'total_tax_amount': {
                    'amount': '0.00',
                    'currency_code': self.currency_code
                }
            }
        }

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(String(36), ForeignKey("carts.id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    cart = relationship("Cart", back_populates="items")
    variant = relationship("ProductVariant")
    
    @property
    def total_amount(self):
        if self.variant and self.variant.price:
            return float(self.variant.price) * self.quantity
        return 0.0
    
    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'variant_id': self.variant_id,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'cost': {
                'total_amount': {
                    'amount': str(self.total_amount),
                    'currency_code': self.cart.currency_code if self.cart else 'USD'
                }
            },
            'merchandise': {
                'id': str(self.variant.id) if self.variant else None,
                'title': self.variant.title if self.variant else None,
                'price': {
                    'amount': str(self.variant.price) if self.variant and self.variant.price else '0.00',
                    'currency_code': self.cart.currency_code if self.cart else 'USD'
                },
                'product': {
                    'id': str(self.variant.product.id) if self.variant and self.variant.product else None,
                    'handle': self.variant.product.handle if self.variant and self.variant.product else None,
                    'title': self.variant.product.title if self.variant and self.variant.product else None,
                    'featured_image': self.variant.product.images[0].to_dict() if self.variant and self.variant.product and self.variant.product.images else None
                }
            } if self.variant else None
        }
