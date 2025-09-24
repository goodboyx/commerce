from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from models.product import Collection, Product, ProductVariant, ProductImage
from schemas.product import CollectionCreate, CollectionResponse
from typing import List, Optional

router = APIRouter(prefix="/collections", tags=["collections"])

@router.get("/", response_model=List[CollectionResponse])
async def get_collections(
    published_only: bool = Query(True, description="공개된 컬렉션만"),
    db: Session = Depends(get_db)
):
    """컬렉션 목록 조회"""
    try:
        query = db.query(Collection)
        
        if published_only:
            query = query.filter(Collection.published == True)
        
        collections = query.order_by(Collection.created_at.desc()).all()
        return [collection.to_dict() for collection in collections]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{handle}", response_model=CollectionResponse)
async def get_collection(handle: str, db: Session = Depends(get_db)):
    """개별 컬렉션 조회"""
    print(Collection)
    try:
        collection = db.query(Collection).filter(Collection.handle == handle).first()
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        return collection.to_dict()
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{handle}/products")
async def get_collection_products(
    handle: str,
    page: int = Query(1, ge=1, description="페이지 번호"),
    per_page: int = Query(20, ge=1, le=100, description="페이지당 항목 수"),
    sort_key: Optional[str] = Query(None, description="정렬 기준 (title, price, created_at)"),
    reverse: bool = Query(False, description="역순 정렬"),
    available_only: bool = Query(True, description="판매 가능한 제품만"),
    db: Session = Depends(get_db)
):
    """컬렉션의 제품 목록 조회"""
    try:
        # 컬렉션 존재 확인
        collection = db.query(Collection).filter(Collection.handle == handle).first()
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        # 제품 쿼리 구성
        query = db.query(Product).join(Product.collections).filter(Collection.id == collection.id)
        
        if available_only:
            query = query.filter(Product.available_for_sale == True)
        
        # 정렬 적용
        if sort_key == "title":
            order_by = Product.title.desc() if reverse else Product.title.asc()
        elif sort_key == "price":
            # 가격 정렬을 위해 subquery 사용하여 최소 가격으로 정렬
            from sqlalchemy import func
            min_price_subquery = db.query(
                ProductVariant.product_id,
                func.min(ProductVariant.price).label('min_price')
            ).group_by(ProductVariant.product_id).subquery()
            
            query = query.join(min_price_subquery, Product.id == min_price_subquery.c.product_id)
            order_by = min_price_subquery.c.min_price.desc() if reverse else min_price_subquery.c.min_price.asc()
        elif sort_key == "created_at":
            order_by = Product.created_at.desc() if reverse else Product.created_at.asc()
        else:
            # 기본 정렬: 생성일 역순
            order_by = Product.created_at.desc()
        
        query = query.order_by(order_by)
        
        # 총 개수 계산
        total = query.count()
        
        # 페이지네이션 적용
        offset = (page - 1) * per_page
        products = query.offset(offset).limit(per_page).all()
        
        # 총 페이지 수 계산
        import math
        pages = math.ceil(total / per_page)
        
        # 제품 데이터 변환
        products_data = []
        for product in products:
            product_dict = product.to_dict()
            products_data.append(product_dict)
        
        return {
            "products": products_data,
            "collection": collection.to_dict(),
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "has_next_page": page < pages,
            "has_previous_page": page > 1
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=CollectionResponse, status_code=201)
async def create_collection(
    collection_data: CollectionCreate,
    db: Session = Depends(get_db)
):
    """새 컬렉션 생성"""
    try:
        # 중복 handle 검사
        existing_collection = db.query(Collection).filter(
            Collection.handle == collection_data.handle
        ).first()
        
        if existing_collection:
            raise HTTPException(status_code=400, detail="Collection with this handle already exists")
        
        collection = Collection(
            handle=collection_data.handle,
            title=collection_data.title,
            description=collection_data.description,
            published=collection_data.published
        )
        
        db.add(collection)
        db.commit()
        db.refresh(collection)
        
        return collection.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{handle}", response_model=CollectionResponse)
async def update_collection(
    handle: str,
    collection_data: CollectionCreate,
    db: Session = Depends(get_db)
):
    """컬렉션 정보 업데이트"""
    try:
        collection = db.query(Collection).filter(Collection.handle == handle).first()
        
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        collection.title = collection_data.title
        collection.description = collection_data.description
        collection.published = collection_data.published
        
        db.commit()
        db.refresh(collection)
        
        return collection.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{handle}")
async def delete_collection(handle: str, db: Session = Depends(get_db)):
    """컬렉션 삭제"""
    try:
        collection = db.query(Collection).filter(Collection.handle == handle).first()
        
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        db.delete(collection)
        db.commit()
        
        return {"message": "Collection deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{handle}/products/{product_id}")
async def add_product_to_collection(
    handle: str,
    product_id: int,
    db: Session = Depends(get_db)
):
    """컬렉션에 제품 추가"""
    try:
        collection = db.query(Collection).filter(Collection.handle == handle).first()
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # 이미 컬렉션에 있는지 확인
        if product in collection.products:
            raise HTTPException(status_code=400, detail="Product already in collection")
        
        collection.products.append(product)
        db.commit()
        
        return {"message": "Product added to collection successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{handle}/products/{product_id}")
async def remove_product_from_collection(
    handle: str,
    product_id: int,
    db: Session = Depends(get_db)
):
    """컬렉션에서 제품 제거"""
    try:
        collection = db.query(Collection).filter(Collection.handle == handle).first()
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # 컬렉션에 있는지 확인
        if product not in collection.products:
            raise HTTPException(status_code=400, detail="Product not in collection")
        
        collection.products.remove(product)
        db.commit()
        
        return {"message": "Product removed from collection successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
