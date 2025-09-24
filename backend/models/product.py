from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, DECIMAL, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

# 다대다 관계를 위한 연결 테이블
product_collections = Table(
    'product_collections',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collections.id'), primary_key=True)
)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    handle = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    description_html = Column(Text)
    vendor = Column(String(255))
    product_type = Column(String(255))
    available_for_sale = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    collections = relationship("Collection", secondary=product_collections, back_populates="products")
    
    def to_dict(self):
        return {
            'id': self.id,
            'handle': self.handle,
            'title': self.title,
            'description': self.description,
            'description_html': self.description_html,
            'vendor': self.vendor,
            'product_type': self.product_type,
            'available_for_sale': self.available_for_sale,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'variants': [variant.to_dict() for variant in self.variants],
            'images': [image.to_dict() for image in self.images],
            'collections': [collection.to_dict() for collection in self.collections],
            'price_range': self.get_price_range(),
            'featured_image': self.images[0].to_dict() if self.images else None
        }
    
    def get_price_range(self):
        if not self.variants:
            return {'min_price': 0, 'max_price': 0}
        
        prices = [float(variant.price) for variant in self.variants if variant.price]
        if not prices:
            return {'min_price': 0, 'max_price': 0}
        
        return {
            'min_price': min(prices),
            'max_price': max(prices)
        }

class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    compare_at_price = Column(DECIMAL(10, 2))
    sku = Column(String(255), unique=True, index=True)
    barcode = Column(String(255))
    inventory_quantity = Column(Integer, default=0)
    weight = Column(DECIMAL(8, 2))
    weight_unit = Column(String(10), default="kg")
    available_for_sale = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    product = relationship("Product", back_populates="variants")
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': self.title,
            'price': float(self.price) if self.price else None,
            'compare_at_price': float(self.compare_at_price) if self.compare_at_price else None,
            'sku': self.sku,
            'barcode': self.barcode,
            'inventory_quantity': self.inventory_quantity,
            'weight': float(self.weight) if self.weight else None,
            'weight_unit': self.weight_unit,
            'available_for_sale': self.available_for_sale,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ProductImage(Base):
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url = Column(String(1000), nullable=False)
    alt_text = Column(String(500))
    width = Column(Integer)
    height = Column(Integer)
    position = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # 관계
    product = relationship("Product", back_populates="images")
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'url': self.url,
            'alt_text': self.alt_text,
            'width': self.width,
            'height': self.height,
            'position': self.position,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Collection(Base):
    __tablename__ = "collections"
    
    id = Column(Integer, primary_key=True, index=True)
    handle = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    sort_order = Column(String(50), default="manual")
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    products = relationship("Product", secondary=product_collections, back_populates="collections")
    
    def to_dict(self):
        return {
            'id': self.id,
            'handle': self.handle,
            'title': self.title,
            'description': self.description,
            'sort_order': self.sort_order,
            'published': self.published,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'path': f'/search/{self.handle}',
            'product_count': len(self.products)
        }
