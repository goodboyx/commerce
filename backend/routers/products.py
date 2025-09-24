from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from services.product_service import ProductService
from schemas.product import (
    ProductCreate, 
    ProductUpdate, 
    ProductResponse, 
    ProductListResponse,
    ProductSearchRequest
)
from typing import List, Optional

router = APIRouter(prefix="/products", tags=["products"])
product_service = ProductService()

@router.get("/", response_model=ProductListResponse)
async def get_products(
    query: Optional[str] = Query(None, description="검색어"),
    sort_key: str = Query("created_at", description="정렬 기준"),
    reverse: bool = Query(False, description="역순 정렬 여부"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    per_page: int = Query(20, ge=1, le=100, description="페이지당 항목 수"),
    collection_id: Optional[int] = Query(None, description="컬렉션 ID"),
    available_only: bool = Query(True, description="판매 가능한 상품만"),
    db: Session = Depends(get_db)
):
    """제품 목록 조회"""
    try:
        result = product_service.get_products(
            db=db,
            query=query,
            sort_key=sort_key,
            reverse=reverse,
            page=page,
            per_page=per_page,
            collection_id=collection_id,
            available_only=available_only
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{handle}", response_model=ProductResponse)
async def get_product(handle: str, db: Session = Depends(get_db)):
    """개별 제품 조회"""
    try:
        product = product_service.get_product_by_handle(db=db, handle=handle)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """새 제품 생성"""
    try:
        product = product_service.create_product(db=db, product_data=product_data)
        return product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{handle}", response_model=ProductResponse)
async def update_product(
    handle: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """제품 정보 업데이트"""
    try:
        product = product_service.update_product(db=db, handle=handle, product_data=product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{handle}")
async def delete_product(handle: str, db: Session = Depends(get_db)):
    """제품 삭제"""
    try:
        success = product_service.delete_product(db=db, handle=handle)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{handle}/recommendations", response_model=List[ProductResponse])
async def get_product_recommendations(
    handle: str,
    limit: int = Query(4, ge=1, le=20, description="추천 제품 수"),
    db: Session = Depends(get_db)
):
    """제품 추천 목록 조회"""
    try:
        recommendations = product_service.get_product_recommendations(
            db=db, 
            handle=handle, 
            limit=limit
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=ProductListResponse)
async def search_products(
    search_request: ProductSearchRequest,
    db: Session = Depends(get_db)
):
    """제품 검색 (POST 방식)"""
    try:
        result = product_service.get_products(
            db=db,
            query=search_request.query,
            sort_key=search_request.sort_key,
            reverse=search_request.reverse,
            page=search_request.page,
            per_page=search_request.per_page,
            collection_id=search_request.collection_id,
            available_only=search_request.available_only
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
