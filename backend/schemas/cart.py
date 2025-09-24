from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class CartItemCreate(BaseModel):
    variant_id: int = Field(..., description="변형 상품 ID")
    quantity: int = Field(..., ge=1, description="수량")

class CartItemUpdate(BaseModel):
    id: int = Field(..., description="장바구니 아이템 ID")
    variant_id: Optional[int] = Field(None, description="변형 상품 ID")
    quantity: int = Field(..., ge=0, description="수량 (0이면 삭제)")

class CartItemResponse(BaseModel):
    id: int
    cart_id: str
    variant_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime
    cost: Dict[str, Any]
    merchandise: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True

class CartCreate(BaseModel):
    user_id: Optional[str] = Field(None, description="사용자 ID")

class CartResponse(BaseModel):
    id: str
    user_id: Optional[str]
    session_id: str
    currency_code: str
    created_at: datetime
    updated_at: datetime
    items: List[CartItemResponse]
    total_quantity: int
    cost: Dict[str, Any]
    
    class Config:
        from_attributes = True

class AddToCartRequest(BaseModel):
    items: List[CartItemCreate] = Field(..., description="추가할 아이템 목록")

class UpdateCartRequest(BaseModel):
    items: List[CartItemUpdate] = Field(..., description="업데이트할 아이템 목록")

class RemoveFromCartRequest(BaseModel):
    item_ids: List[int] = Field(..., description="제거할 아이템 ID 목록")
