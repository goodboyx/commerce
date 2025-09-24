-- 완전한 샘플 데이터 삽입 스크립트
-- Vercel Commerce와 호환되는 실제 데이터

-- 컬렉션 데이터 삽입
INSERT INTO collections (handle, title, description, published, created_at, updated_at) VALUES
('hidden-homepage-featured-items', 'Hidden Homepage Featured Items', 'Featured products for homepage display', true, NOW(), NOW()),
('featured', 'Featured Products', 'Our most popular and recommended products', true, NOW(), NOW()),
('new-arrivals', 'New Arrivals', 'Latest products added to our store', true, NOW(), NOW()),
('bestsellers', 'Best Sellers', 'Top selling products this month', true, NOW(), NOW()),
('on-sale', 'On Sale', 'Products with special discounts', true, NOW(), NOW()),
('electronics', 'Electronics', 'Electronic devices and accessories', true, NOW(), NOW()),
('clothing', 'Clothing', 'Fashion and apparel items', true, NOW(), NOW()),
('home-garden', 'Home & Garden', 'Home improvement and garden supplies', true, NOW(), NOW());

-- 제품 데이터 삽입
INSERT INTO products (handle, title, description, description_html, vendor, product_type, available_for_sale, created_at, updated_at) VALUES
-- Featured Products
('wireless-headphones', 'Premium Wireless Headphones', 'High-quality wireless headphones with noise cancellation and premium sound quality. Perfect for music lovers and professionals.', '<p>High-quality wireless headphones with <strong>noise cancellation</strong> and premium sound quality.</p><ul><li>40-hour battery life</li><li>Active noise cancellation</li><li>Premium sound quality</li><li>Comfortable fit</li></ul>', 'AudioTech', 'Electronics', true, NOW() - INTERVAL 1 DAY, NOW()),

('smart-watch', 'Smart Fitness Watch', 'Advanced smartwatch with health monitoring, GPS tracking, and smartphone connectivity. Track your fitness goals and stay connected.', '<p>Advanced smartwatch with <strong>health monitoring</strong>, GPS tracking, and smartphone connectivity.</p><ul><li>Heart rate monitoring</li><li>GPS tracking</li><li>Water resistant</li><li>7-day battery life</li></ul>', 'TechWear', 'Electronics', true, NOW() - INTERVAL 2 DAY, NOW()),

('organic-coffee', 'Premium Organic Coffee Beans', 'Single-origin organic coffee beans roasted to perfection. Rich, smooth flavor with notes of chocolate and caramel.', '<p>Single-origin <strong>organic coffee beans</strong> roasted to perfection.</p><ul><li>100% organic</li><li>Single-origin</li><li>Medium roast</li><li>Fair trade certified</li></ul>', 'Mountain Roasters', 'Food & Beverage', true, NOW() - INTERVAL 3 DAY, NOW()),

('yoga-mat', 'Eco-Friendly Yoga Mat', 'Premium yoga mat made from sustainable materials. Non-slip surface and extra cushioning for comfortable practice.', '<p>Premium yoga mat made from <strong>sustainable materials</strong>.</p><ul><li>Non-slip surface</li><li>Extra cushioning</li><li>Eco-friendly</li><li>Easy to clean</li></ul>', 'ZenLife', 'Sports & Fitness', true, NOW() - INTERVAL 4 DAY, NOW()),

('leather-backpack', 'Vintage Leather Backpack', 'Handcrafted leather backpack with vintage styling. Perfect for work, travel, or everyday use. Durable and stylish.', '<p>Handcrafted <strong>leather backpack</strong> with vintage styling.</p><ul><li>Genuine leather</li><li>Multiple compartments</li><li>Laptop compatible</li><li>Vintage design</li></ul>', 'Heritage Crafts', 'Accessories', true, NOW() - INTERVAL 5 DAY, NOW()),

-- New Arrivals
('bluetooth-speaker', 'Portable Bluetooth Speaker', 'Compact wireless speaker with powerful sound and long battery life. Perfect for outdoor adventures and home use.', '<p>Compact wireless speaker with <strong>powerful sound</strong> and long battery life.</p><ul><li>360-degree sound</li><li>Waterproof design</li><li>12-hour battery</li><li>Voice assistant</li></ul>', 'SoundWave', 'Electronics', true, NOW() - INTERVAL 1 HOUR, NOW()),

('running-shoes', 'Professional Running Shoes', 'Lightweight running shoes with advanced cushioning and breathable design. Perfect for serious runners and fitness enthusiasts.', '<p>Lightweight running shoes with <strong>advanced cushioning</strong> and breathable design.</p><ul><li>Lightweight design</li><li>Advanced cushioning</li><li>Breathable mesh</li><li>Durable sole</li></ul>', 'RunPro', 'Footwear', true, NOW() - INTERVAL 2 HOUR, NOW()),

('desk-lamp', 'LED Desk Lamp', 'Modern LED desk lamp with adjustable brightness and color temperature. Perfect for work and study environments.', '<p>Modern <strong>LED desk lamp</strong> with adjustable brightness and color temperature.</p><ul><li>Adjustable brightness</li><li>Color temperature control</li><li>USB charging port</li><li>Modern design</li></ul>', 'LightTech', 'Home & Office', true, NOW() - INTERVAL 3 HOUR, NOW()),

-- Electronics
('smartphone', 'Latest Smartphone', 'Cutting-edge smartphone with advanced camera system, fast processor, and all-day battery life.', '<p>Cutting-edge smartphone with <strong>advanced camera system</strong>, fast processor, and all-day battery life.</p><ul><li>Triple camera system</li><li>Fast processor</li><li>All-day battery</li><li>5G connectivity</li></ul>', 'TechCorp', 'Electronics', true, NOW() - INTERVAL 6 DAY, NOW()),

('laptop', 'Professional Laptop', 'High-performance laptop for professionals and creators. Fast processor, ample storage, and premium display.', '<p>High-performance laptop for <strong>professionals and creators</strong>.</p><ul><li>Fast processor</li><li>16GB RAM</li><li>512GB SSD</li><li>4K display</li></ul>', 'CompuTech', 'Electronics', true, NOW() - INTERVAL 7 DAY, NOW());

-- 제품 변형 데이터 삽입
INSERT INTO product_variants (product_id, title, price, compare_at_price, sku, inventory_quantity, weight, weight_unit, available_for_sale, created_at, updated_at) VALUES
-- Wireless Headphones
(1, 'Black', 199.99, 249.99, 'WH-001-BLK', 50, 0.3, 'kg', true, NOW(), NOW()),
(1, 'White', 199.99, 249.99, 'WH-001-WHT', 30, 0.3, 'kg', true, NOW(), NOW()),

-- Smart Watch
(2, '42mm Black', 299.99, 349.99, 'SW-001-42-BLK', 25, 0.05, 'kg', true, NOW(), NOW()),
(2, '42mm Silver', 299.99, 349.99, 'SW-001-42-SLV', 20, 0.05, 'kg', true, NOW(), NOW()),
(2, '46mm Black', 329.99, 379.99, 'SW-001-46-BLK', 15, 0.06, 'kg', true, NOW(), NOW()),

-- Organic Coffee
(3, '250g Bag', 24.99, NULL, 'COF-001-250', 100, 0.25, 'kg', true, NOW(), NOW()),
(3, '500g Bag', 45.99, 49.99, 'COF-001-500', 75, 0.5, 'kg', true, NOW(), NOW()),
(3, '1kg Bag', 85.99, 95.99, 'COF-001-1000', 40, 1.0, 'kg', true, NOW(), NOW()),

-- Yoga Mat
(4, 'Purple', 49.99, 59.99, 'YM-001-PUR', 30, 1.2, 'kg', true, NOW(), NOW()),
(4, 'Blue', 49.99, 59.99, 'YM-001-BLU', 25, 1.2, 'kg', true, NOW(), NOW()),
(4, 'Green', 49.99, 59.99, 'YM-001-GRN', 35, 1.2, 'kg', true, NOW(), NOW()),

-- Leather Backpack
(5, 'Brown', 149.99, 179.99, 'LB-001-BRN', 20, 1.5, 'kg', true, NOW(), NOW()),
(5, 'Black', 149.99, 179.99, 'LB-001-BLK', 15, 1.5, 'kg', true, NOW(), NOW()),

-- Bluetooth Speaker
(6, 'Black', 79.99, 99.99, 'BS-001-BLK', 40, 0.8, 'kg', true, NOW(), NOW()),
(6, 'Blue', 79.99, 99.99, 'BS-001-BLU', 35, 0.8, 'kg', true, NOW(), NOW()),

-- Running Shoes
(7, 'Size 8 - Black', 129.99, 149.99, 'RS-001-8-BLK', 10, 0.4, 'kg', true, NOW(), NOW()),
(7, 'Size 9 - Black', 129.99, 149.99, 'RS-001-9-BLK', 15, 0.4, 'kg', true, NOW(), NOW()),
(7, 'Size 10 - Black', 129.99, 149.99, 'RS-001-10-BLK', 12, 0.4, 'kg', true, NOW(), NOW()),
(7, 'Size 8 - White', 129.99, 149.99, 'RS-001-8-WHT', 8, 0.4, 'kg', true, NOW(), NOW()),
(7, 'Size 9 - White', 129.99, 149.99, 'RS-001-9-WHT', 10, 0.4, 'kg', true, NOW(), NOW()),

-- Desk Lamp
(8, 'White', 89.99, NULL, 'DL-001-WHT', 25, 1.0, 'kg', true, NOW(), NOW()),
(8, 'Black', 89.99, NULL, 'DL-001-BLK', 20, 1.0, 'kg', true, NOW(), NOW()),

-- Smartphone
(9, '128GB - Black', 799.99, 899.99, 'SP-001-128-BLK', 30, 0.2, 'kg', true, NOW(), NOW()),
(9, '256GB - Black', 899.99, 999.99, 'SP-001-256-BLK', 25, 0.2, 'kg', true, NOW(), NOW()),
(9, '128GB - White', 799.99, 899.99, 'SP-001-128-WHT', 20, 0.2, 'kg', true, NOW(), NOW()),

-- Laptop
(10, '16GB RAM / 512GB SSD', 1299.99, 1499.99, 'LP-001-16-512', 15, 2.0, 'kg', true, NOW(), NOW()),
(10, '32GB RAM / 1TB SSD', 1599.99, 1799.99, 'LP-001-32-1TB', 10, 2.0, 'kg', true, NOW(), NOW());

-- 제품 이미지 데이터 삽입
INSERT INTO product_images (product_id, url, alt_text, width, height, position, created_at) VALUES
-- Wireless Headphones
(1, 'https://via.placeholder.com/800x600/1a1a1a/ffffff?text=Wireless+Headphones', 'Premium Wireless Headphones', 800, 600, 1, NOW()),
(1, 'https://via.placeholder.com/800x600/2a2a2a/ffffff?text=Headphones+Side+View', 'Headphones Side View', 800, 600, 2, NOW()),

-- Smart Watch
(2, 'https://via.placeholder.com/800x600/0066cc/ffffff?text=Smart+Watch', 'Smart Fitness Watch', 800, 600, 1, NOW()),
(2, 'https://via.placeholder.com/800x600/0077dd/ffffff?text=Watch+Features', 'Watch Features', 800, 600, 2, NOW()),

-- Organic Coffee
(3, 'https://via.placeholder.com/800x600/8B4513/ffffff?text=Organic+Coffee', 'Premium Organic Coffee Beans', 800, 600, 1, NOW()),
(3, 'https://via.placeholder.com/800x600/A0522D/ffffff?text=Coffee+Beans', 'Coffee Beans Close-up', 800, 600, 2, NOW()),

-- Yoga Mat
(4, 'https://via.placeholder.com/800x600/9932cc/ffffff?text=Yoga+Mat', 'Eco-Friendly Yoga Mat', 800, 600, 1, NOW()),
(4, 'https://via.placeholder.com/800x600/aa44dd/ffffff?text=Mat+Texture', 'Mat Texture Detail', 800, 600, 2, NOW()),

-- Leather Backpack
(5, 'https://via.placeholder.com/800x600/8B4513/ffffff?text=Leather+Backpack', 'Vintage Leather Backpack', 800, 600, 1, NOW()),
(5, 'https://via.placeholder.com/800x600/A0522D/ffffff?text=Backpack+Interior', 'Backpack Interior', 800, 600, 2, NOW()),

-- Bluetooth Speaker
(6, 'https://via.placeholder.com/800x600/333333/ffffff?text=Bluetooth+Speaker', 'Portable Bluetooth Speaker', 800, 600, 1, NOW()),

-- Running Shoes
(7, 'https://via.placeholder.com/800x600/ff6b35/ffffff?text=Running+Shoes', 'Professional Running Shoes', 800, 600, 1, NOW()),

-- Desk Lamp
(8, 'https://via.placeholder.com/800x600/f4f4f4/333333?text=Desk+Lamp', 'LED Desk Lamp', 800, 600, 1, NOW()),

-- Smartphone
(9, 'https://via.placeholder.com/800x600/1a1a1a/ffffff?text=Smartphone', 'Latest Smartphone', 800, 600, 1, NOW()),

-- Laptop
(10, 'https://via.placeholder.com/800x600/silver/333333?text=Professional+Laptop', 'Professional Laptop', 800, 600, 1, NOW());

-- 제품-컬렉션 연결 데이터 삽입
INSERT INTO product_collections (product_id, collection_id) VALUES
-- Hidden Homepage Featured Items (가장 중요한 컬렉션!)
(1, 1), -- Wireless Headphones
(2, 1), -- Smart Watch  
(3, 1), -- Organic Coffee
(4, 1), -- Yoga Mat
(5, 1), -- Leather Backpack

-- Featured Products
(1, 2), -- Wireless Headphones
(2, 2), -- Smart Watch
(3, 2), -- Organic Coffee
(5, 2), -- Leather Backpack
(9, 2), -- Smartphone

-- New Arrivals
(6, 3), -- Bluetooth Speaker
(7, 3), -- Running Shoes
(8, 3), -- Desk Lamp

-- Electronics
(1, 6), -- Wireless Headphones
(2, 6), -- Smart Watch
(6, 6), -- Bluetooth Speaker
(8, 6), -- Desk Lamp
(9, 6), -- Smartphone
(10, 6), -- Laptop

-- On Sale (제품들이 compare_at_price를 가지고 있음)
(1, 5), -- Wireless Headphones (할인 중)
(2, 5), -- Smart Watch (할인 중)
(3, 5), -- Organic Coffee (할인 중)
(4, 5), -- Yoga Mat (할인 중)
(5, 5), -- Leather Backpack (할인 중)
(6, 5), -- Bluetooth Speaker (할인 중)
(7, 5), -- Running Shoes (할인 중)
(9, 5), -- Smartphone (할인 중)
(10, 5); -- Laptop (할인 중)

-- 사용자 데이터 (테스트용)
INSERT INTO users (email, first_name, last_name, phone, created_at, updated_at) VALUES
('test@example.com', 'Test', 'User', '+1234567890', NOW(), NOW()),
('admin@example.com', 'Admin', 'User', '+1234567891', NOW(), NOW());

-- 장바구니 데이터 (테스트용)
INSERT INTO carts (user_id, session_id, currency_code, created_at, updated_at) VALUES
(1, 'test-session-1', 'USD', NOW(), NOW()),
(NULL, 'guest-session-1', 'USD', NOW(), NOW());

-- 장바구니 아이템 데이터 (테스트용)
INSERT INTO cart_items (cart_id, variant_id, quantity, created_at, updated_at) VALUES
(1, 1, 1, NOW(), NOW()), -- Wireless Headphones Black
(1, 5, 2, NOW(), NOW()), -- Organic Coffee 250g
(2, 3, 1, NOW(), NOW()); -- Smart Watch 42mm Black

-- 주문 데이터 (테스트용)
INSERT INTO orders (user_id, email, total_amount, currency_code, status, created_at, updated_at) VALUES
(1, 'test@example.com', 249.97, 'USD', 'pending', NOW() - INTERVAL 1 DAY, NOW()),
(1, 'test@example.com', 199.99, 'USD', 'completed', NOW() - INTERVAL 7 DAY, NOW());

-- 주문 아이템 데이터 (테스트용)
INSERT INTO order_items (order_id, variant_id, quantity, price, created_at, updated_at) VALUES
(1, 1, 1, 199.99, NOW() - INTERVAL 1 DAY, NOW()), -- Wireless Headphones
(1, 5, 2, 24.99, NOW() - INTERVAL 1 DAY, NOW()), -- Coffee x2
(2, 3, 1, 199.99, NOW() - INTERVAL 7 DAY, NOW()); -- Smart Watch

-- 데이터 확인 쿼리 (주석 처리됨)
/*
-- 컬렉션별 제품 수 확인
SELECT c.handle, c.title, COUNT(pc.product_id) as product_count
FROM collections c
LEFT JOIN product_collections pc ON c.id = pc.collection_id
GROUP BY c.id, c.handle, c.title
ORDER BY c.handle;

-- hidden-homepage-featured-items 컬렉션의 제품들 확인
SELECT p.handle, p.title, p.vendor, pv.price
FROM products p
JOIN product_collections pc ON p.id = pc.product_id
JOIN collections c ON pc.collection_id = c.id
JOIN product_variants pv ON p.id = pv.product_id
WHERE c.handle = 'hidden-homepage-featured-items'
ORDER BY p.title;
*/
