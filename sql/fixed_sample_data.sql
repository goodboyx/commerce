-- 완전히 수정된 샘플 데이터
-- 실제 작동하는 이미지 URL 사용

USE commerce_db;

-- 기존 데이터 삭제
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;
TRUNCATE TABLE cart_items;
TRUNCATE TABLE carts;
TRUNCATE TABLE product_collections;
TRUNCATE TABLE product_images;
TRUNCATE TABLE product_variants;
TRUNCATE TABLE products;
TRUNCATE TABLE collections;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- 컬렉션 데이터 삽입 (hidden-homepage-carousel 포함!)
INSERT INTO collections (handle, title, description, published, created_at, updated_at) VALUES
('hidden-homepage-featured-items', 'Hidden Homepage Featured Items', 'Featured products for homepage display', true, NOW(), NOW()),
('hidden-homepage-carousel', 'Hidden Homepage Carousel', 'Carousel products for homepage banner', true, NOW(), NOW()),
('featured', 'Featured Products', 'Our most popular and recommended products', true, NOW(), NOW()),
('new-arrivals', 'New Arrivals', 'Latest products added to our store', true, NOW(), NOW()),
('bestsellers', 'Best Sellers', 'Top selling products this month', true, NOW(), NOW()),
('on-sale', 'On Sale', 'Products with special discounts', true, NOW(), NOW()),
('electronics', 'Electronics', 'Electronic devices and accessories', true, NOW(), NOW()),
('clothing', 'Clothing', 'Fashion and apparel items', true, NOW(), NOW());

-- 제품 데이터 삽입 (실제 이미지 URL 사용)
INSERT INTO products (handle, title, description, description_html, vendor, product_type, available_for_sale, created_at, updated_at) VALUES
-- Featured Products
('wireless-headphones', 'Premium Wireless Headphones', 'High-quality wireless headphones with noise cancellation and premium sound quality. Perfect for music lovers and professionals.', '<p>High-quality wireless headphones with <strong>noise cancellation</strong> and premium sound quality.</p><ul><li>40-hour battery life</li><li>Active noise cancellation</li><li>Premium sound quality</li><li>Comfortable fit</li></ul>', 'AudioTech', 'Electronics', true, NOW() - INTERVAL 1 DAY, NOW()),

('smart-watch', 'Smart Fitness Watch', 'Advanced smartwatch with health monitoring, GPS tracking, and smartphone connectivity. Track your fitness goals and stay connected.', '<p>Advanced smartwatch with <strong>health monitoring</strong>, GPS tracking, and smartphone connectivity.</p><ul><li>Heart rate monitoring</li><li>GPS tracking</li><li>Water resistant</li><li>7-day battery life</li></ul>', 'TechWear', 'Electronics', true, NOW() - INTERVAL 2 DAY, NOW()),

('organic-coffee', 'Premium Organic Coffee Beans', 'Single-origin organic coffee beans roasted to perfection. Rich, smooth flavor with notes of chocolate and caramel.', '<p>Single-origin <strong>organic coffee beans</strong> roasted to perfection.</p><ul><li>100% organic</li><li>Single-origin</li><li>Medium roast</li><li>Fair trade certified</li></ul>', 'Mountain Roasters', 'Food & Beverage', true, NOW() - INTERVAL 3 DAY, NOW()),

('yoga-mat', 'Eco-Friendly Yoga Mat', 'Premium yoga mat made from sustainable materials. Non-slip surface and extra cushioning for comfortable practice.', '<p>Premium yoga mat made from <strong>sustainable materials</strong>.</p><ul><li>Non-slip surface</li><li>Extra cushioning</li><li>Eco-friendly</li><li>Easy to clean</li></ul>', 'ZenLife', 'Sports & Fitness', true, NOW() - INTERVAL 4 DAY, NOW()),

('leather-backpack', 'Vintage Leather Backpack', 'Handcrafted leather backpack with vintage styling. Perfect for work, travel, or everyday use. Durable and stylish.', '<p>Handcrafted <strong>leather backpack</strong> with vintage styling.</p><ul><li>Genuine leather</li><li>Multiple compartments</li><li>Laptop compatible</li><li>Vintage design</li></ul>', 'Heritage Crafts', 'Accessories', true, NOW() - INTERVAL 5 DAY, NOW()),

-- Carousel Products (새로 추가!)
('gaming-laptop', 'High-Performance Gaming Laptop', 'Ultimate gaming laptop with RTX graphics, fast processor, and RGB keyboard. Perfect for gaming and creative work.', '<p>Ultimate gaming laptop with <strong>RTX graphics</strong>, fast processor, and RGB keyboard.</p><ul><li>RTX 4070 Graphics</li><li>Intel i7 Processor</li><li>32GB RAM</li><li>1TB NVMe SSD</li></ul>', 'GameTech', 'Electronics', true, NOW() - INTERVAL 1 HOUR, NOW()),

('wireless-earbuds', 'Pro Wireless Earbuds', 'Premium wireless earbuds with active noise cancellation and wireless charging case. Crystal clear sound quality.', '<p>Premium wireless earbuds with <strong>active noise cancellation</strong> and wireless charging case.</p><ul><li>Active noise cancellation</li><li>Wireless charging</li><li>30-hour battery</li><li>Water resistant</li></ul>', 'AudioPro', 'Electronics', true, NOW() - INTERVAL 2 HOUR, NOW()),

('mechanical-keyboard', 'RGB Mechanical Keyboard', 'Professional mechanical keyboard with RGB backlighting and tactile switches. Perfect for gaming and typing.', '<p>Professional mechanical keyboard with <strong>RGB backlighting</strong> and tactile switches.</p><ul><li>Mechanical switches</li><li>RGB backlighting</li><li>Programmable keys</li><li>Durable construction</li></ul>', 'KeyMaster', 'Electronics', true, NOW() - INTERVAL 3 HOUR, NOW()),

-- Additional Products
('bluetooth-speaker', 'Portable Bluetooth Speaker', 'Compact wireless speaker with powerful sound and long battery life. Perfect for outdoor adventures and home use.', '<p>Compact wireless speaker with <strong>powerful sound</strong> and long battery life.</p><ul><li>360-degree sound</li><li>Waterproof design</li><li>12-hour battery</li><li>Voice assistant</li></ul>', 'SoundWave', 'Electronics', true, NOW() - INTERVAL 4 HOUR, NOW()),

('running-shoes', 'Professional Running Shoes', 'Lightweight running shoes with advanced cushioning and breathable design. Perfect for serious runners and fitness enthusiasts.', '<p>Lightweight running shoes with <strong>advanced cushioning</strong> and breathable design.</p><ul><li>Lightweight design</li><li>Advanced cushioning</li><li>Breathable mesh</li><li>Durable sole</li></ul>', 'RunPro', 'Footwear', true, NOW() - INTERVAL 5 HOUR, NOW());

-- 제품 변형 데이터 삽입
INSERT INTO product_variants (product_id, title, price, compare_at_price, sku, inventory_quantity, weight, weight_unit, available_for_sale, created_at, updated_at) VALUES
-- Wireless Headphones
(1, 'Black', 199.99, 249.99, 'WH-001-BLK', 50, 0.3, 'kg', true, NOW(), NOW()),
(1, 'White', 199.99, 249.99, 'WH-001-WHT', 30, 0.3, 'kg', true, NOW(), NOW()),

-- Smart Watch
(2, '42mm Black', 299.99, 349.99, 'SW-001-42-BLK', 25, 0.05, 'kg', true, NOW(), NOW()),
(2, '42mm Silver', 299.99, 349.99, 'SW-001-42-SLV', 20, 0.05, 'kg', true, NOW(), NOW()),

-- Organic Coffee
(3, '250g Bag', 24.99, NULL, 'COF-001-250', 100, 0.25, 'kg', true, NOW(), NOW()),
(3, '500g Bag', 45.99, 49.99, 'COF-001-500', 75, 0.5, 'kg', true, NOW(), NOW()),

-- Yoga Mat
(4, 'Purple', 49.99, 59.99, 'YM-001-PUR', 30, 1.2, 'kg', true, NOW(), NOW()),
(4, 'Blue', 49.99, 59.99, 'YM-001-BLU', 25, 1.2, 'kg', true, NOW(), NOW()),

-- Leather Backpack
(5, 'Brown', 149.99, 179.99, 'LB-001-BRN', 20, 1.5, 'kg', true, NOW(), NOW()),
(5, 'Black', 149.99, 179.99, 'LB-001-BLK', 15, 1.5, 'kg', true, NOW(), NOW()),

-- Gaming Laptop
(6, '16GB RAM / 512GB SSD', 1599.99, 1799.99, 'GL-001-16-512', 10, 2.5, 'kg', true, NOW(), NOW()),
(6, '32GB RAM / 1TB SSD', 1999.99, 2299.99, 'GL-001-32-1TB', 5, 2.5, 'kg', true, NOW(), NOW()),

-- Wireless Earbuds
(7, 'Black', 149.99, 179.99, 'WE-001-BLK', 40, 0.05, 'kg', true, NOW(), NOW()),
(7, 'White', 149.99, 179.99, 'WE-001-WHT', 35, 0.05, 'kg', true, NOW(), NOW()),

-- Mechanical Keyboard
(8, 'Black RGB', 129.99, 149.99, 'MK-001-BLK', 25, 1.0, 'kg', true, NOW(), NOW()),
(8, 'White RGB', 129.99, 149.99, 'MK-001-WHT', 20, 1.0, 'kg', true, NOW(), NOW()),

-- Bluetooth Speaker
(9, 'Black', 79.99, 99.99, 'BS-001-BLK', 40, 0.8, 'kg', true, NOW(), NOW()),
(9, 'Blue', 79.99, 99.99, 'BS-001-BLU', 35, 0.8, 'kg', true, NOW(), NOW()),

-- Running Shoes
(10, 'Size 9 - Black', 129.99, 149.99, 'RS-001-9-BLK', 15, 0.4, 'kg', true, NOW(), NOW()),
(10, 'Size 10 - Black', 129.99, 149.99, 'RS-001-10-BLK', 12, 0.4, 'kg', true, NOW(), NOW());

-- 제품 이미지 데이터 삽입 (실제 작동하는 이미지 URL 사용)
INSERT INTO product_images (product_id, url, alt_text, width, height, position, created_at) VALUES
-- Wireless Headphones (Unsplash 이미지)
(1, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=600&fit=crop', 'Premium Wireless Headphones', 800, 600, 1, NOW()),
(1, 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&h=600&fit=crop', 'Headphones Side View', 800, 600, 2, NOW()),

-- Smart Watch
(2, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&h=600&fit=crop', 'Smart Fitness Watch', 800, 600, 1, NOW()),
(2, 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800&h=600&fit=crop', 'Watch Features', 800, 600, 2, NOW()),

-- Organic Coffee
(3, 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&h=600&fit=crop', 'Premium Organic Coffee Beans', 800, 600, 1, NOW()),
(3, 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&h=600&fit=crop', 'Coffee Beans Close-up', 800, 600, 2, NOW()),

-- Yoga Mat
(4, 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=600&fit=crop', 'Eco-Friendly Yoga Mat', 800, 600, 1, NOW()),

-- Leather Backpack
(5, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&h=600&fit=crop', 'Vintage Leather Backpack', 800, 600, 1, NOW()),

-- Gaming Laptop
(6, 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&h=600&fit=crop', 'High-Performance Gaming Laptop', 800, 600, 1, NOW()),

-- Wireless Earbuds
(7, 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&h=600&fit=crop', 'Pro Wireless Earbuds', 800, 600, 1, NOW()),

-- Mechanical Keyboard
(8, 'https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=800&h=600&fit=crop', 'RGB Mechanical Keyboard', 800, 600, 1, NOW()),

-- Bluetooth Speaker
(9, 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&h=600&fit=crop', 'Portable Bluetooth Speaker', 800, 600, 1, NOW()),

-- Running Shoes
(10, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=600&fit=crop', 'Professional Running Shoes', 800, 600, 1, NOW());

-- 제품-컬렉션 연결 데이터 삽입
INSERT INTO product_collections (product_id, collection_id) VALUES
-- Hidden Homepage Featured Items (컬렉션 ID: 1)
(1, 1), -- Wireless Headphones
(2, 1), -- Smart Watch  
(3, 1), -- Organic Coffee
(4, 1), -- Yoga Mat
(5, 1), -- Leather Backpack

-- Hidden Homepage Carousel (컬렉션 ID: 2) - 새로 추가!
(6, 2), -- Gaming Laptop
(7, 2), -- Wireless Earbuds
(8, 2), -- Mechanical Keyboard
(1, 2), -- Wireless Headphones (중복 가능)
(2, 2), -- Smart Watch (중복 가능)

-- Featured Products (컬렉션 ID: 3)
(1, 3), -- Wireless Headphones
(2, 3), -- Smart Watch
(6, 3), -- Gaming Laptop
(7, 3), -- Wireless Earbuds

-- New Arrivals (컬렉션 ID: 4)
(6, 4), -- Gaming Laptop
(7, 4), -- Wireless Earbuds
(8, 4), -- Mechanical Keyboard

-- Electronics (컬렉션 ID: 7)
(1, 7), -- Wireless Headphones
(2, 7), -- Smart Watch
(6, 7), -- Gaming Laptop
(7, 7), -- Wireless Earbuds
(8, 7), -- Mechanical Keyboard
(9, 7), -- Bluetooth Speaker

-- On Sale (컬렉션 ID: 6) - 할인 제품들
(1, 6), -- Wireless Headphones
(2, 6), -- Smart Watch
(4, 6), -- Yoga Mat
(5, 6), -- Leather Backpack
(6, 6), -- Gaming Laptop
(7, 6), -- Wireless Earbuds
(8, 6), -- Mechanical Keyboard
(9, 6), -- Bluetooth Speaker
(10, 6); -- Running Shoes

-- 사용자 데이터 (테스트용)
INSERT INTO users (email, first_name, last_name, phone, created_at, updated_at) VALUES
('test@example.com', 'Test', 'User', '+1234567890', NOW(), NOW()),
('admin@example.com', 'Admin', 'User', '+1234567891', NOW(), NOW()),
('customer@example.com', 'John', 'Doe', '+1234567892', NOW(), NOW());

-- 장바구니 데이터 (테스트용)
INSERT INTO carts (id, user_id, session_id, currency_code, created_at, updated_at) VALUES
('cart-test-001', 1, 'test-session-1', 'USD', NOW(), NOW()),
('cart-guest-001', NULL, 'guest-session-1', 'USD', NOW(), NOW());

-- 장바구니 아이템 데이터 (테스트용)
INSERT INTO cart_items (cart_id, variant_id, quantity, created_at, updated_at) VALUES
('cart-test-001', 1, 1, NOW(), NOW()), -- Wireless Headphones Black
('cart-test-001', 5, 2, NOW(), NOW()), -- Organic Coffee 250g
('cart-guest-001', 3, 1, NOW(), NOW()); -- Smart Watch 42mm Black

-- 주문 데이터 (테스트용)
INSERT INTO orders (id, user_id, email, total_amount, currency_code, status, created_at, updated_at) VALUES
('order-001', 1, 'test@example.com', 249.97, 'USD', 'pending', NOW() - INTERVAL 1 DAY, NOW()),
('order-002', 1, 'test@example.com', 199.99, 'USD', 'completed', NOW() - INTERVAL 7 DAY, NOW());

-- 주문 아이템 데이터 (테스트용)
INSERT INTO order_items (order_id, variant_id, quantity, price, created_at, updated_at) VALUES
('order-001', 1, 1, 199.99, NOW() - INTERVAL 1 DAY, NOW()), -- Wireless Headphones
('order-001', 5, 2, 24.99, NOW() - INTERVAL 1 DAY, NOW()), -- Coffee x2
('order-002', 3, 1, 199.99, NOW() - INTERVAL 7 DAY, NOW()); -- Smart Watch

-- 데이터 확인 쿼리
SELECT 'Sample data loaded successfully!' as message;

-- 컬렉션별 제품 수 확인
SELECT 
    c.handle, 
    c.title, 
    COUNT(pc.product_id) as product_count
FROM collections c
LEFT JOIN product_collections pc ON c.id = pc.collection_id
GROUP BY c.id, c.handle, c.title
ORDER BY c.handle;
