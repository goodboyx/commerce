from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

class ProductImageBase(BaseModel):
    url: str = Field(..., description="이미지 URL")
    alt_text: Optional[str] = Field(None, description="대체 텍스트")
    width: Optional[int] = Field(None, description="이미지 너비")
    height: Optional[int] = Field(None, description="이미지 높이")

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageResponse(ProductImageBase):
    id: int
    position: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductVariantBase(BaseModel):
    title: str = Field(..., description="변형 상품명")
    price: Decimal = Field(..., description="가격")
    compare_at_price: Optional[Decimal] = Field(None, description="비교 가격")
    sku: Optional[str] = Field(None, description="SKU")
    barcode: Optional[str] = Field(None, description="바코드")
    inventory_quantity: int = Field(0, description="재고 수량")
    weight: Optional[Decimal] = Field(None, description="무게")
    weight_unit: str = Field("kg", description="무게 단위")
    available_for_sale: bool = Field(True, description="판매 가능 여부")

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[Decimal] = None
    compare_at_price: Optional[Decimal] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    inventory_quantity: Optional[int] = None
    weight: Optional[Decimal] = None
    weight_unit: Optional[str] = None
    available_for_sale: Optional[bool] = None

class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CollectionBase(BaseModel):
    handle: str = Field(..., description="컬렉션 핸들")
    title: str = Field(..., description="컬렉션명")
    description: Optional[str] = Field(None, description="컬렉션 설명")
    published: bool = Field(True, description="공개 여부")

class CollectionCreate(CollectionBase):
    pass

class CollectionResponse(CollectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    path: str
    product_count: int
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    handle: str = Field(..., description="제품 핸들")
    title: str = Field(..., description="제품명")
    description: Optional[str] = Field(None, description="제품 설명")
    description_html: Optional[str] = Field(None, description="HTML 제품 설명")
    vendor: Optional[str] = Field(None, description="제조사")
    product_type: Optional[str] = Field(None, description="제품 타입")
    available_for_sale: bool = Field(True, description="판매 가능 여부")
    
    @validator('handle')
    def validate_handle(cls, v):
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Handle must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower()

class ProductCreate(ProductBase):
    variants: List[ProductVariantCreate] = Field([], description="변형 상품 목록")
    images: List[ProductImageCreate] = Field([], description="이미지 목록")
    collection_ids: List[int] = Field([], description="컬렉션 ID 목록")

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[str] = None
    available_for_sale: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    variants: List[ProductVariantResponse] = []
    images: List[ProductImageResponse] = []
    collections: List[CollectionResponse] = []
    
    # 계산된 필드들
    price_range: Dict[str, Any] = Field(default_factory=dict)
    featured_image: Optional[ProductImageResponse] = None
    
    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int
    pages: int

class ProductSearchRequest(BaseModel):
    query: Optional[str] = Field(None, description="검색어")
    sort_key: str = Field("created_at", description="정렬 기준")
    reverse: bool = Field(False, description="역순 정렬 여부")
    page: int = Field(1, ge=1, description="페이지 번호")
    per_page: int = Field(20, ge=1, le=100, description="페이지당 항목 수")
    collection_id: Optional[int] = Field(None, description="컬렉션 ID")
    available_only: bool = Field(True, description="판매 가능한 상품만")
