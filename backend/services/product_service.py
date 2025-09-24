from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models.product import Product, ProductVariant, ProductImage, Collection
from schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional, Dict, Any
import math

class ProductService:
    
    def get_products(
        self, 
        db: Session,
        query: Optional[str] = None,
        sort_key: str = "created_at",
        reverse: bool = False,
        page: int = 1,
        per_page: int = 20,
        collection_id: Optional[int] = None,
        available_only: bool = True
    ) -> Dict[str, Any]:
        """제품 목록 조회"""
        
        # 기본 쿼리
        products_query = db.query(Product)
        
        # 판매 가능한 상품만 필터링
        if available_only:
            products_query = products_query.filter(Product.available_for_sale == True)
        
        # 검색 필터 적용
        if query:
            products_query = products_query.filter(
                or_(
                    Product.title.ilike(f'%{query}%'),
                    Product.description.ilike(f'%{query}%'),
                    Product.vendor.ilike(f'%{query}%'),
                    Product.product_type.ilike(f'%{query}%')
                )
            )
        
        # 컬렉션 필터 적용
        if collection_id:
            products_query = products_query.join(Product.collections).filter(
                Collection.id == collection_id
            )
        
        # 정렬 적용
        if sort_key == "title":
            order_column = Product.title
        elif sort_key == "created_at":
            order_column = Product.created_at
        elif sort_key == "updated_at":
            order_column = Product.updated_at
        else:
            order_column = Product.created_at
            
        if reverse:
            products_query = products_query.order_by(order_column.desc())
        else:
            products_query = products_query.order_by(order_column.asc())
        
        # 총 개수 계산
        total = products_query.count()
        
        # 페이지네이션 적용
        offset = (page - 1) * per_page
        products = products_query.offset(offset).limit(per_page).all()
        
        # 총 페이지 수 계산
        pages = math.ceil(total / per_page)
        
        return {
            "products": [product.to_dict() for product in products],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages
        }
    
    def get_product_by_handle(self, db: Session, handle: str) -> Optional[Dict[str, Any]]:
        """핸들로 제품 조회"""
        product = db.query(Product).filter(Product.handle == handle).first()
        return product.to_dict() if product else None
    
    def get_product_by_id(self, db: Session, product_id: int) -> Optional[Dict[str, Any]]:
        """ID로 제품 조회"""
        product = db.query(Product).filter(Product.id == product_id).first()
        return product.to_dict() if product else None
    
    def create_product(self, db: Session, product_data: ProductCreate) -> Dict[str, Any]:
        """새 제품 생성"""
        
        # 중복 handle 검사
        existing_product = db.query(Product).filter(Product.handle == product_data.handle).first()
        if existing_product:
            raise ValueError("Product with this handle already exists")
        
        # 제품 생성
        product = Product(
            handle=product_data.handle,
            title=product_data.title,
            description=product_data.description,
            description_html=product_data.description_html,
            vendor=product_data.vendor,
            product_type=product_data.product_type,
            available_for_sale=product_data.available_for_sale
        )
        
        db.add(product)
        db.flush()  # ID 생성을 위해
        
        # 변형 상품 추가
        for variant_data in product_data.variants:
            variant = ProductVariant(
                product_id=product.id,
                title=variant_data.title,
                price=variant_data.price,
                compare_at_price=variant_data.compare_at_price,
                sku=variant_data.sku,
                barcode=variant_data.barcode,
                inventory_quantity=variant_data.inventory_quantity,
                weight=variant_data.weight,
                weight_unit=variant_data.weight_unit,
                available_for_sale=variant_data.available_for_sale
            )
            db.add(variant)
        
        # 이미지 추가
        for i, image_data in enumerate(product_data.images):
            image = ProductImage(
                product_id=product.id,
                url=image_data.url,
                alt_text=image_data.alt_text,
                width=image_data.width,
                height=image_data.height,
                position=i
            )
            db.add(image)
        
        # 컬렉션 연결
        if product_data.collection_ids:
            collections = db.query(Collection).filter(
                Collection.id.in_(product_data.collection_ids)
            ).all()
            product.collections.extend(collections)
        
        db.commit()
        db.refresh(product)
        
        return product.to_dict()
    
    def update_product(self, db: Session, handle: str, product_data: ProductUpdate) -> Optional[Dict[str, Any]]:
        """제품 정보 업데이트"""
        product = db.query(Product).filter(Product.handle == handle).first()
        
        if not product:
            return None
        
        # 제품 정보 업데이트
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        
        return product.to_dict()
    
    def delete_product(self, db: Session, handle: str) -> bool:
        """제품 삭제"""
        product = db.query(Product).filter(Product.handle == handle).first()
        
        if not product:
            return False
        
        db.delete(product)
        db.commit()
        
        return True
    
    def get_product_recommendations(self, db: Session, handle: str, limit: int = 4) -> List[Dict[str, Any]]:
        """제품 추천 목록 조회"""
        
        # 현재 제품 조회
        current_product = db.query(Product).filter(Product.handle == handle).first()
        
        if not current_product:
            return []
        
        # 간단한 추천 로직: 같은 컬렉션의 다른 제품들
        recommended_products = []
        
        if current_product.collections:
            for collection in current_product.collections:
                for product in collection.products:
                    if product.id != current_product.id and len(recommended_products) < limit:
                        recommended_products.append(product)
        
        # 컬렉션이 없거나 추천 제품이 부족한 경우 최신 제품으로 보완
        if len(recommended_products) < limit:
            additional_products = db.query(Product)\
                .filter(
                    and_(
                        Product.id != current_product.id,
                        Product.available_for_sale == True
                    )
                )\
                .order_by(Product.created_at.desc())\
                .limit(limit - len(recommended_products))\
                .all()
            recommended_products.extend(additional_products)
        
        return [product.to_dict() for product in recommended_products[:limit]]
