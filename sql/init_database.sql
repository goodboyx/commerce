-- MariaDB 커머스 데이터베이스 초기화 스크립트

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS commerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 사용자 생성 및 권한 부여
CREATE USER IF NOT EXISTS 'commerce_user'@'localhost' IDENTIFIED BY 'commerce_password';
CREATE USER IF NOT EXISTS 'commerce_user'@'%' IDENTIFIED BY 'commerce_password';

GRANT ALL PRIVILEGES ON commerce_db.* TO 'commerce_user'@'localhost';
GRANT ALL PRIVILEGES ON commerce_db.* TO 'commerce_user'@'%';

FLUSH PRIVILEGES;

-- 데이터베이스 사용
USE commerce_db;

-- 테이블 생성 (SQLAlchemy가 자동으로 생성하지만 수동으로도 가능)

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    default_address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login DATETIME,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- 컬렉션 테이블
CREATE TABLE IF NOT EXISTS collections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    handle VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    sort_order VARCHAR(50) DEFAULT 'manual',
    published BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_handle (handle),
    INDEX idx_published (published)
);

-- 제품 테이블
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    handle VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    description_html TEXT,
    vendor VARCHAR(255),
    product_type VARCHAR(255),
    available_for_sale BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_handle (handle),
    INDEX idx_title (title),
    INDEX idx_vendor (vendor),
    INDEX idx_product_type (product_type),
    INDEX idx_available_for_sale (available_for_sale),
    INDEX idx_created_at (created_at)
);

-- 제품 변형 테이블
CREATE TABLE IF NOT EXISTS product_variants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    compare_at_price DECIMAL(10,2),
    sku VARCHAR(255) UNIQUE,
    barcode VARCHAR(255),
    inventory_quantity INT DEFAULT 0,
    weight DECIMAL(8,2),
    weight_unit VARCHAR(10) DEFAULT 'kg',
    available_for_sale BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_sku (sku),
    INDEX idx_price (price),
    INDEX idx_available_for_sale (available_for_sale)
);

-- 제품 이미지 테이블
CREATE TABLE IF NOT EXISTS product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    url VARCHAR(1000) NOT NULL,
    alt_text VARCHAR(500),
    width INT,
    height INT,
    position INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_position (position)
);

-- 제품-컬렉션 연결 테이블
CREATE TABLE IF NOT EXISTS product_collections (
    product_id INT,
    collection_id INT,
    PRIMARY KEY (product_id, collection_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
);

-- 장바구니 테이블
CREATE TABLE IF NOT EXISTS carts (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    session_id VARCHAR(255),
    currency_code VARCHAR(3) DEFAULT 'USD',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id)
);

-- 장바구니 아이템 테이블
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id VARCHAR(36) NOT NULL,
    variant_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (variant_id) REFERENCES product_variants(id) ON DELETE CASCADE,
    INDEX idx_cart_id (cart_id),
    INDEX idx_variant_id (variant_id),
    UNIQUE KEY unique_cart_variant (cart_id, variant_id)
);

-- 주문 테이블
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(36) PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id VARCHAR(36),
    email VARCHAR(255) NOT NULL,
    status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
    subtotal_amount DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    shipping_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    currency_code VARCHAR(3) DEFAULT 'USD',
    payment_id VARCHAR(255),
    payment_method VARCHAR(50),
    shipping_address TEXT,
    billing_address TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    shipped_at DATETIME,
    delivered_at DATETIME,
    INDEX idx_order_number (order_number),
    INDEX idx_user_id (user_id),
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_payment_status (payment_status),
    INDEX idx_created_at (created_at)
);

-- 주문 아이템 테이블
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    variant_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    product_title VARCHAR(500),
    variant_title VARCHAR(255),
    product_handle VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (variant_id) REFERENCES product_variants(id),
    INDEX idx_order_id (order_id),
    INDEX idx_variant_id (variant_id)
);

-- 샘플 데이터 삽입

-- 컬렉션 샘플 데이터
INSERT INTO collections (handle, title, description, published) VALUES
('featured', '추천 상품', '엄선된 추천 상품들', TRUE),
('new-arrivals', '신상품', '최신 출시 상품들', TRUE),
('electronics', '전자제품', '다양한 전자제품', TRUE),
('clothing', '의류', '패션 의류 컬렉션', TRUE),
('accessories', '액세서리', '다양한 액세서리', TRUE);

-- 제품 샘플 데이터
INSERT INTO products (handle, title, description, vendor, product_type, available_for_sale) VALUES
('wireless-headphones', '무선 헤드폰', '고품질 무선 블루투스 헤드폰', 'TechBrand', '전자제품', TRUE),
('cotton-t-shirt', '코튼 티셔츠', '100% 순면 편안한 티셔츠', 'FashionCo', '의류', TRUE),
('smartphone-case', '스마트폰 케이스', '내구성 강한 스마트폰 보호 케이스', 'AccessoryPlus', '액세서리', TRUE),
('running-shoes', '러닝화', '편안한 운동화', 'SportsBrand', '신발', TRUE),
('laptop-bag', '노트북 가방', '15인치 노트북용 가방', 'BagMaker', '가방', TRUE);

-- 제품 변형 샘플 데이터
INSERT INTO product_variants (product_id, title, price, sku, inventory_quantity, available_for_sale) VALUES
(1, '무선 헤드폰 - 블랙', 99.99, 'WH-001-BLK', 50, TRUE),
(1, '무선 헤드폰 - 화이트', 99.99, 'WH-001-WHT', 30, TRUE),
(2, '코튼 티셔츠 - S', 19.99, 'CT-001-S', 100, TRUE),
(2, '코튼 티셔츠 - M', 19.99, 'CT-001-M', 150, TRUE),
(2, '코튼 티셔츠 - L', 19.99, 'CT-001-L', 120, TRUE),
(3, '스마트폰 케이스 - 투명', 15.99, 'SC-001-CLR', 200, TRUE),
(3, '스마트폰 케이스 - 블랙', 15.99, 'SC-001-BLK', 180, TRUE),
(4, '러닝화 - 260mm', 79.99, 'RS-001-260', 40, TRUE),
(4, '러닝화 - 270mm', 79.99, 'RS-001-270', 35, TRUE),
(5, '노트북 가방 - 블랙', 49.99, 'LB-001-BLK', 25, TRUE);

-- 제품 이미지 샘플 데이터
INSERT INTO product_images (product_id, url, alt_text, position) VALUES
(1, 'https://via.placeholder.com/400x400/000000/FFFFFF?text=Headphones', '무선 헤드폰', 0),
(2, 'https://via.placeholder.com/400x400/FF0000/FFFFFF?text=T-Shirt', '코튼 티셔츠', 0),
(3, 'https://via.placeholder.com/400x400/0000FF/FFFFFF?text=Phone+Case', '스마트폰 케이스', 0),
(4, 'https://via.placeholder.com/400x400/00FF00/FFFFFF?text=Shoes', '러닝화', 0),
(5, 'https://via.placeholder.com/400x400/FFFF00/000000?text=Laptop+Bag', '노트북 가방', 0);

-- 제품-컬렉션 연결
INSERT INTO product_collections (product_id, collection_id) VALUES
(1, 1), (1, 3), -- 무선 헤드폰: 추천상품, 전자제품
(2, 2), (2, 4), -- 코튼 티셔츠: 신상품, 의류
(3, 1), (3, 5), -- 스마트폰 케이스: 추천상품, 액세서리
(4, 2), (4, 4), -- 러닝화: 신상품, 의류
(5, 1), (5, 5); -- 노트북 가방: 추천상품, 액세서리

-- 인덱스 최적화
OPTIMIZE TABLE products;
OPTIMIZE TABLE product_variants;
OPTIMIZE TABLE collections;
OPTIMIZE TABLE carts;
OPTIMIZE TABLE cart_items;
OPTIMIZE TABLE orders;
OPTIMIZE TABLE order_items;
