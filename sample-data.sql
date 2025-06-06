-- Sample data for the piata_ro database

-- Insert sample users
INSERT INTO users (username, password, salt, email, first_name, last_name, avatar, bio, phone, location, is_admin, created_at, is_verified)
VALUES
  ('admin', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'admin@piata.ro', 'Admin', 'User', 'https://randomuser.me/api/portraits/men/1.jpg', 'Administrator account', '+40721000001', 'Bucharest', TRUE, NOW(), TRUE),
  ('john_doe', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'john@example.com', 'John', 'Doe', 'https://randomuser.me/api/portraits/men/2.jpg', 'Regular seller with lots of items', '+40721000002', 'Cluj-Napoca', FALSE, NOW(), TRUE),
  ('jane_smith', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'jane@example.com', 'Jane', 'Smith', 'https://randomuser.me/api/portraits/women/1.jpg', 'Looking for great deals', '+40721000003', 'Timisoara', FALSE, NOW(), TRUE),
  ('alex_popescu', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'alex@example.com', 'Alex', 'Popescu', 'https://randomuser.me/api/portraits/men/3.jpg', 'Car enthusiast', '+40721000004', 'Brasov', FALSE, NOW(), TRUE),
  ('maria_ionescu', '$2a$10$XQxBtVxj7aJZ3qE7U9JZp.uQZA0Lj6G1CHm8tVrfQK5xbgs3uJgMK', 'salt123', 'maria@example.com', 'Maria', 'Ionescu', 'https://randomuser.me/api/portraits/women/2.jpg', 'Real estate agent', '+40721000005', 'Constanta', FALSE, NOW(), TRUE);

-- Delete existing category data from 'categories' table
DELETE FROM categories;
-- Reset auto-increment counter for 'categories' table (SQLite specific)
-- This command is for SQLite. If using a different DB, adjust accordingly.
DELETE FROM sqlite_sequence WHERE name='categories';

-- Insert new Romanian categories
-- Main Categories (Expected IDs 1-11)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Imobiliare', 'imobiliare', 'fas fa-home', '#4CAF50', NULL),
('Auto, Moto și Ambarcațiuni', 'auto-moto-ambarcatiuni', 'fas fa-car', '#2196F3', NULL),
('Electronice și Electrocasnice', 'electronice-electrocasnice', 'fas fa-laptop', '#FF9800', NULL),
('Locuri de Muncă', 'locuri-de-munca', 'fas fa-briefcase', '#9C27B0', NULL),
('Servicii, Afaceri, Echipamente Firme', 'servicii-afaceri-echipamente', 'fas fa-concierge-bell', '#3F51B5', NULL),
('Modă și Frumusețe', 'moda-frumusete', 'fas fa-tshirt', '#E91E63', NULL),
('Casă și Grădină', 'casa-gradina', 'fas fa-leaf', '#8BC34A', NULL),
('Sport, Timp Liber, Artă', 'sport-timp-liber-arta', 'fas fa-futbol', '#FFC107', NULL),
('Mama și Copilul', 'mama-copilul', 'fas fa-child', '#00BCD4', NULL),
('Animale de Companie', 'animale-companie', 'fas fa-paw', '#607D8B', NULL),
('Agro și Industrie', 'agro-industrie', 'fas fa-tractor', '#795548', NULL);

-- Subcategories (Expected IDs start from 12 onwards)

-- Subcategories for 'Imobiliare' (Parent ID: 1)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Apartamente de vânzare', 'apartamente-vanzare', 'far fa-building', '#4CAF50', 1),
('Apartamente de închiriat', 'apartamente-inchiriat', 'far fa-building', '#4CAF50', 1),
('Case de vânzare', 'case-vanzare', 'fas fa-home', '#4CAF50', 1),
('Case de închiriat', 'case-inchiriat', 'fas fa-home', '#4CAF50', 1),
('Terenuri', 'terenuri', 'fas fa-map-marked-alt', '#4CAF50', 1),
('Spații comerciale/Birouri', 'spatii-comerciale-birouri', 'fas fa-store', '#4CAF50', 1),
('Cazare/Turism', 'cazare-turism', 'fas fa-hotel', '#4CAF50', 1);

-- Subcategories for 'Auto, Moto și Ambarcațiuni' (Parent ID: 2)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Autoturisme', 'autoturisme', 'fas fa-car-side', '#2196F3', 2),
('Motociclete/Scutere/ATV', 'moto-scutere-atv', 'fas fa-motorcycle', '#2196F3', 2),
('Rulote/Autorulote', 'rulote-autorulote', 'fas fa-caravan', '#2196F3', 2),
('Camioane/Utilaje', 'camioane-utilaje', 'fas fa-truck', '#2196F3', 2),
('Ambarcațiuni', 'ambarcatiuni', 'fas fa-ship', '#2196F3', 2),
('Piese Auto', 'piese-auto', 'fas fa-cogs', '#2196F3', 2),
('Servicii Auto', 'servicii-auto', 'fas fa-tools', '#2196F3', 2);

-- Subcategories for 'Electronice și Electrocasnice' (Parent ID: 3)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Telefoane', 'telefoane', 'fas fa-mobile-alt', '#FF9800', 3),
('Calculatoare/Laptopuri', 'calculatoare-laptopuri', 'fas fa-laptop', '#FF9800', 3),
('TV/Audio/Video', 'tv-audio-video', 'fas fa-tv', '#FF9800', 3),
('Electrocasnice Mari', 'electrocasnice-mari', 'fas fa-blender-phone', '#FF9800', 3), -- blender-phone is not standard, maybe 'fas fa-server' or specific items
('Electrocasnice Mici', 'electrocasnice-mici', 'fas fa-coffee', '#FF9800', 3),
('Jocuri/Console', 'jocuri-console', 'fas fa-gamepad', '#FF9800', 3),
('Aparate Foto/Video', 'aparate-foto-video', 'fas fa-camera-retro', '#FF9800', 3);

-- Subcategories for 'Locuri de Muncă' (Parent ID: 4)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Oferte de angajare', 'oferte-angajare', 'fas fa-briefcase', '#9C27B0', 4),
('CV-uri/Cereri de angajare', 'cv-cereri-angajare', 'far fa-file-alt', '#9C27B0', 4),
('Servicii de recrutare', 'servicii-recrutare', 'fas fa-users-cog', '#9C27B0', 4);

-- Subcategories for 'Modă și Frumusețe' (Parent ID: 6)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Haine Damă', 'haine-dama', 'fas fa-female', '#E91E63', 6),
('Haine Bărbați', 'haine-barbati', 'fas fa-male', '#E91E63', 6),
('Haine Copii', 'haine-copii', 'fas fa-child', '#E91E63', 6),
('Încălțăminte', 'incaltaminte', 'fas fa-shoe-prints', '#E91E63', 6),
('Accesorii (Genți, Ceasuri, Bijuterii)', 'accesorii-genti-ceasuri-bijuterii', 'fas fa-gem', '#E91E63', 6),
('Cosmetice/Parfumuri', 'cosmetice-parfumuri', 'fas fa-magic', '#E91E63', 6);

-- Subcategories for 'Casă și Grădină' (Parent ID: 7)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Mobilă/Decorațiuni', 'mobila-decoratiuni', 'fas fa-couch', '#8BC34A', 7),
('Unelte/Materiale de construcții', 'unelte-materiale-constructii', 'fas fa-tools', '#8BC34A', 7),
('Articole menaj/Curățenie', 'articole-menaj-curatenie', 'fas fa-broom', '#8BC34A', 7),
('Plante/Amenajări grădină', 'plante-amenajari-gradina', 'fas fa-seedling', '#8BC34A', 7);

-- Subcategories for 'Mama și Copilul' (Parent ID: 9)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Cărucioare/Scaune auto', 'carucioare-scaune-auto', 'fas fa-baby-carriage', '#00BCD4', 9),
('Haine/Încălțăminte copii', 'haine-incaltaminte-copii-mama', 'fas fa-child', '#00BCD4', 9), -- Renamed slug slightly
('Jucării', 'jucarii', 'fas fa-shapes', '#00BCD4', 9),
('Articole școlare', 'articole-scolare', 'fas fa-graduation-cap', '#00BCD4', 9);

-- Subcategories for 'Animale de Companie' (Parent ID: 10)
INSERT INTO categories (name, slug, icon, color, parent_id) VALUES
('Câini', 'caini', 'fas fa-dog', '#607D8B', 10),
('Pisici', 'pisici', 'fas fa-cat', '#607D8B', 10),
('Păsări', 'pasari', 'fas fa-dove', '#607D8B', 10),
('Hrană/Accesorii Animale', 'hrana-accesorii-animale', 'fas fa-bone', '#607D8B', 10);

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

-- IMPORTANT: Review and update category_id and subcategory_id in the
-- 'INSERT INTO listings' statements below to match the new category IDs
-- if specific subcategory relations are important for sample data.
-- Main category IDs (1-8) used in original listings should still map to the correct top-level category.
