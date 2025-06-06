-- Sample data for the piata_ro database

-- Insert sample users
INSERT INTO users (username, password, salt, email, first_name, last_name, avatar, bio, phone, location, is_admin, created_at, is_verified)
VALUES
  ('admin', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'admin@piata.ro', 'Admin', 'User', 'https://randomuser.me/api/portraits/men/1.jpg', 'Administrator account', '+40721000001', 'Bucharest', TRUE, NOW(), TRUE),
  ('john_doe', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'john@example.com', 'John', 'Doe', 'https://randomuser.me/api/portraits/men/2.jpg', 'Regular seller with lots of items', '+40721000002', 'Cluj-Napoca', FALSE, NOW(), TRUE),
  ('jane_smith', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'jane@example.com', 'Jane', 'Smith', 'https://randomuser.me/api/portraits/women/1.jpg', 'Looking for great deals', '+40721000003', 'Timisoara', FALSE, NOW(), TRUE),
  ('alex_popescu', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'alex@example.com', 'Alex', 'Popescu', 'https://randomuser.me/api/portraits/men/3.jpg', 'Car enthusiast', '+40721000004', 'Brasov', FALSE, NOW(), TRUE),
  ('maria_ionescu', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'maria@example.com', 'Maria', 'Ionescu', 'https://randomuser.me/api/portraits/women/2.jpg', 'Real estate agent', '+40721000005', 'Constanta', FALSE, NOW(), TRUE);

-- Insert sample categories
INSERT INTO categories (name, slug, icon, color)
VALUES
  ('Real Estate', 'real-estate', 'home', '#4CAF50'),
  ('Vehicles', 'vehicles', 'car', '#2196F3'),
  ('Electronics', 'electronics', 'laptop', '#FF9800'),
  ('Jobs', 'jobs', 'briefcase', '#9C27B0'),
  ('Services', 'services', 'tools', '#795548'),
  ('Fashion', 'fashion', 'shirt', '#E91E63'),
  ('Home & Garden', 'home-garden', 'flower', '#8BC34A'),
  ('Sports & Leisure', 'sports-leisure', 'bicycle', '#00BCD4');

-- Insert subcategories
INSERT INTO categories (name, slug, icon, color, parent_id)
VALUES
  ('Apartments', 'apartments', 'apartment', '#4CAF50', 1),
  ('Houses', 'houses', 'house', '#4CAF50', 1),
  ('Land', 'land', 'terrain', '#4CAF50', 1),
  ('Commercial', 'commercial', 'store', '#4CAF50', 1),
  
  ('Cars', 'cars', 'car', '#2196F3', 2),
  ('Motorcycles', 'motorcycles', 'motorcycle', '#2196F3', 2),
  ('Trucks', 'trucks', 'truck', '#2196F3', 2),
  ('Auto Parts', 'auto-parts', 'engine', '#2196F3', 2),
  
  ('Phones', 'phones', 'phone', '#FF9800', 3),
  ('Computers', 'computers', 'computer', '#FF9800', 3),
  ('TV & Audio', 'tv-audio', 'tv', '#FF9800', 3),
  ('Gaming', 'gaming', 'gamepad', '#FF9800', 3);

-- Insert sample listings
INSERT INTO listings (title, description, price, currency, location, images, user_id, category_id, subcategory_id, status, created_at, updated_at, expires_at, is_premium, views)
VALUES
  ('Modern 2-bedroom apartment in central Bucharest', 'Beautiful, newly renovated apartment with 2 bedrooms, living room, kitchen, and bathroom. Located in the heart of Bucharest, close to all amenities.', 120000, 'EUR', 'Bucharest, Sector 1', ARRAY['https://images.unsplash.com/photo-1522708323590-d24dbb6b0267', 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688'], 2, 1, 1, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', TRUE, 156),
  
  ('2018 BMW 320d, excellent condition', 'Selling my 2018 BMW 320d with 75,000 km. Full service history, no accidents, one owner. Diesel, automatic transmission, leather seats, navigation.', 22500, 'EUR', 'Cluj-Napoca', ARRAY['https://images.unsplash.com/photo-1555215695-3004980ad54e', 'https://images.unsplash.com/photo-1520031441872-956195f7e400'], 4, 2, 5, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', TRUE, 243),
  
  ('iPhone 13 Pro, 256GB, like new', 'Selling my iPhone 13 Pro, 256GB, graphite color. Used for 6 months, like new condition, no scratches. Comes with original box, charger, and case.', 3500, 'RON', 'Timisoara', ARRAY['https://images.unsplash.com/photo-1632661674596-618e45e68f10'], 3, 3, 9, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', FALSE, 87),
  
  ('Software Developer - Remote Work', 'We are looking for an experienced Software Developer to join our team. Remote work possible. Requirements: 3+ years of experience with JavaScript, React, Node.js.', 0, 'RON', 'Remote', ARRAY[], 5, 4, NULL, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', TRUE, 312),
  
  ('Professional House Cleaning Services', 'Offering professional house cleaning services in Brasov. Regular cleaning, deep cleaning, move-in/move-out cleaning. Experienced, reliable, and affordable.', 150, 'RON', 'Brasov', ARRAY['https://images.unsplash.com/photo-1581578731548-c64695cc6952'], 4, 5, NULL, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', FALSE, 45),
  
  ('Designer Leather Jacket, Size M', 'Selling a beautiful designer leather jacket, size M. Black color, excellent condition, worn only a few times. Original price 2000 RON.', 1200, 'RON', 'Constanta', ARRAY['https://images.unsplash.com/photo-1551028719-00167b16eac5'], 5, 6, NULL, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', FALSE, 67),
  
  ('Garden furniture set', 'Selling a garden furniture set: table and 4 chairs. Made of high-quality wood, weather-resistant. Used for one season, excellent condition.', 800, 'RON', 'Bucharest, Sector 3', ARRAY['https://images.unsplash.com/photo-1595429035839-c99c298ffdde'], 2, 7, NULL, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', FALSE, 34),
  
  ('Mountain Bike - Trek Marlin 7', 'Selling my Trek Marlin 7 mountain bike. Size L, 29" wheels, hydraulic disc brakes. Used for one season, excellent condition.', 2500, 'RON', 'Cluj-Napoca', ARRAY['https://images.unsplash.com/photo-1576435728678-68d0fbf94e91'], 3, 8, NULL, 'active', NOW(), NOW(), NOW() + INTERVAL '30 days', TRUE, 128);

-- Insert sample messages
INSERT INTO messages (sender_id, receiver_id, listing_id, content, created_at, is_read)
VALUES
  (3, 2, 1, 'Hi, is this apartment still available?', NOW() - INTERVAL '2 days', TRUE),
  (2, 3, 1, 'Yes, it is still available. Would you like to schedule a viewing?', NOW() - INTERVAL '1 day', TRUE),
  (3, 2, 1, 'Yes, I would. How about tomorrow at 5 PM?', NOW() - INTERVAL '1 day', FALSE),
  
  (4, 3, 3, 'Is the price negotiable?', NOW() - INTERVAL '3 days', TRUE),
  (3, 4, 3, 'I can go down to 3300 RON, but that''s my final price.', NOW() - INTERVAL '2 days', TRUE),
  
  (5, 4, 5, 'Do you offer services in Sibiu as well?', NOW(), FALSE);

-- Insert sample favorites
INSERT INTO favorites (user_id, listing_id, created_at)
VALUES
  (3, 1, NOW() - INTERVAL '3 days'),
  (3, 2, NOW() - INTERVAL '2 days'),
  (4, 3, NOW() - INTERVAL '1 day'),
  (5, 4, NOW()),
  (2, 5, NOW() - INTERVAL '4 days');
