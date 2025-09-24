from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from models.order import OrderStatus, PaymentStatus

class OrderItemResponse(BaseModel):
    id: int
    order_id: str
    variant_id: int
    quantity: int
    price: Decimal
    total_amount: Decimal
    product_title: Optional[str]
    variant_title: Optional[str]
    product_handle: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    cart_id: str = Field(..., description="장바구니 ID")
    email: EmailStr = Field(..., description="이메일 주소")
    shipping_address: str = Field(..., description="배송 주소")
    billing_address: Optional[str] = Field(None, description="청구 주소")
    notes: Optional[str] = Field(None, description="주문 메모")

class OrderResponse(BaseModel):
    id: str
    order_number: str
    user_id: Optional[str]
    email: str
    status: str
    payment_status: str
    subtotal_amount: Decimal
    tax_amount: Decimal
    shipping_amount: Decimal
    total_amount: Decimal
    currency_code: str
    payment_id: Optional[str]
    payment_method: Optional[str]
    shipping_address: str
    billing_address: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    per_page: int
    pages: int

class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., description="주문 상태")

class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus = Field(..., description="결제 상태")
    payment_id: Optional[str] = Field(None, description="결제 ID")
    payment_method: Optional[str] = Field(None, description="결제 방법")

class OrderSummary(BaseModel):
    """주문 요약 정보"""
    total_orders: int
    pending_orders: int
    confirmed_orders: int
    shipped_orders: int
    delivered_orders: int
    cancelled_orders: int
    total_revenue: Decimal
    average_order_value: Decimal
