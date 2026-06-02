-- =============================================
-- PRODUCT_CATEGORY
-- =============================================
INSERT INTO PRODUCT_CATEGORY (category_name) VALUES
('Beverages'),
('Snacks & Chips'),
('Canned Goods'),
('Personal Care'),
('Cleaning Supplies'),
('Condiments & Sauces'),
('Instant Noodles & Pasta'),
('Dairy & Eggs'),
('Frozen Foods'),
('Rice & Grains');

-- =============================================
-- SUPPLIER
-- =============================================
INSERT INTO SUPPLIER (supplier_name, contact_number, supplier_street, supplier_barangay, supplier_city, supplier_province) VALUES
('Monde Nissin Corporation', '09171234501', '160 Ibayo Tipas', 'Ibayo Tipas', 'Taguig', 'Metro Manila'),
('Universal Robina Corporation', '09181234502', '110 E. Rodriguez Jr. Ave', 'Bagumbayan', 'Quezon City', 'Metro Manila'),
('San Miguel Brewery Inc.', '09191234503', '40 San Miguel Ave', 'Mandaluyong', 'Mandaluyong', 'Metro Manila'),
('Nestlé Philippines Inc.', '09201234504', '22 St. Francis St', 'Mandaluyong', 'Mandaluyong', 'Metro Manila'),
('Century Pacific Food Inc.', '09211234505', '7th Avenue corner 9th Street', 'Bonifacio Global City', 'Taguig', 'Metro Manila'),
('Del Monte Philippines', '09221234506', 'Km. 33 McArthur Highway', 'Tibungco', 'Davao City', 'Davao del Sur'),
('Unilever Philippines', '09231234507', 'Unilever House, 30th St', 'Bonifacio Global City', 'Taguig', 'Metro Manila'),
('Alaska Milk Corporation', '09241234508', 'Pioneer St', 'Mandaluyong', 'Mandaluyong', 'Metro Manila'),
('Rebisco Group of Companies', '09251234509', '29 Matimyas St', 'Sta. Mesa', 'Manila', 'Metro Manila'),
('Fly Ace Corporation', '09261234510', '7 Annapolis St', 'Greenhills', 'San Juan', 'Metro Manila');

-- =============================================
-- CUSTOMER
-- =============================================
INSERT INTO CUSTOMER (customer_name, contact_number, customer_street, customer_barangay, customer_city, customer_province) VALUES
('Maria Santos', '09171110001', '12 Rizal St', 'Ilawod', 'Legazpi City', 'Albay'),
('Jose Reyes', '09182220002', '45 Mabini Ave', 'Bagumbayan', 'Legazpi City', 'Albay'),
('Ana Cruz', '09193330003', '7 Bonifacio St', 'Puro', 'Legazpi City', 'Albay'),
('Carlo Dela Cruz', '09204440004', '88 Quezon Blvd', 'Cabangan', 'Legazpi City', 'Albay'),
('Liza Mendoza', '09215550005', '3 Sto. Niño St', 'Mabinit', 'Legazpi City', 'Albay'),
('Ramon Villanueva', '09226660006', '55 Magsaysay Ave', 'Rawis', 'Legazpi City', 'Albay'),
('Cristina Bautista', '09237770007', '21 Del Pilar St', 'Pinaric', 'Legazpi City', 'Albay'),
('Eduardo Torres', '09248880008', '9 Luna St', 'Bigaa', 'Legazpi City', 'Albay'),
('Rosa Aquino', '09259990009', '66 Burgos St', 'Taysan', 'Legazpi City', 'Albay'),
('Felix Soriano', '09260000010', '14 Rizal Ave', 'Bitano', 'Legazpi City', 'Albay'),
('Marites Gonzales', '09171111011', '33 Aguinaldo St', 'Old Albay', 'Legazpi City', 'Albay'),
('Dante Ferrer', '09182222012', '17 Osmeña St', 'Buyuan', 'Legazpi City', 'Albay'),
('Nelia Ramos', '09193333013', '5 Paterno St', 'Arimbay', 'Legazpi City', 'Albay'),
('Arnold Castillo', '09204444014', '90 Roxas Blvd', 'Estanza', 'Legazpi City', 'Albay'),
('Teresita Navarro', '09215555015', '28 Ocampo St', 'Homapon', 'Legazpi City', 'Albay'),
('Rodrigo Lim', '09226666016', '11 Dimaporo St', 'Banquerohan', 'Legazpi City', 'Albay'),
('Gloria Padilla', '09237777017', '63 Mapagmahal St', 'Sagpon', 'Legazpi City', 'Albay'),
('Benjamin Uy', '09248888018', '44 Katipunan St', 'Bonot', 'Legazpi City', 'Albay'),
('Rosario Mercado', '09259999019', '8 Lapu-Lapu St', 'Cruzada', 'Legazpi City', 'Albay'),
('Dennis Tan', '09260000020', '77 Gen. Luna St', 'Dita', 'Legazpi City', 'Albay'),
('Shirley Ramirez', '09171112021', '20 Mabini St', 'Gogon', 'Legazpi City', 'Albay'),
('Alfredo Jimenez', '09182223022', '39 Rizal St', 'Imperial Court', 'Legazpi City', 'Albay'),
('Concepcion Flores', '09193334023', '2 National Highway', 'Landco', 'Legazpi City', 'Albay'),
('Victor Pascual', '09204445024', '58 Claro M. Recto St', 'Pablacion', 'Legazpi City', 'Albay'),
('Imelda Aguilar', '09215556025', '16 Mabini Extension', 'San Joaquin', 'Legazpi City', 'Albay');

-- =============================================
-- PRODUCT
-- =============================================
INSERT INTO PRODUCT (product_name, price, stock_quantity, category_id) VALUES
-- Beverages (1)
('Coca-Cola 1.5L', 65.00, 120, 1),
('Royal Tru-Orange 1L', 45.00, 95, 1),
('C2 Green Tea Apple 500ml', 28.00, 150, 1),
('Nestea Iced Tea Lemon 500ml', 25.00, 130, 1),
('Zesto Orange Juice 250ml', 12.00, 200, 1),
('Pepsi 1.5L', 62.00, 100, 1),
('Wilkins Distilled Water 1L', 22.00, 180, 1),
-- Snacks & Chips (2)
('Nova Country Cheddar 78g', 35.00, 110, 2),
('Piattos Cheese 85g', 38.00, 105, 2),
('Boy Bawang Garlic 100g', 28.00, 140, 2),
('Chippy BBQ 110g', 32.00, 125, 2),
('Rebisco Crackers 33g', 10.00, 300, 2),
('Skyflakes Crackers 400g', 58.00, 90, 2),
-- Canned Goods (3)
('Century Tuna Flakes in Oil 180g', 42.00, 200, 3),
('Argentina Corned Beef 260g', 85.00, 160, 3),
('Ligo Sardines in Tomato Sauce 155g', 24.00, 250, 3),
('Del Monte Pork and Beans 230g', 38.00, 175, 3),
('CDO Liver Spread 165g', 30.00, 140, 3),
-- Personal Care (4)
('Head & Shoulders Shampoo 180ml', 115.00, 60, 4),
('Safeguard Bar Soap 135g', 42.00, 120, 4),
('Colgate Toothpaste 150ml', 72.00, 85, 4),
('Dove Body Wash 400ml', 180.00, 40, 4),
('Gillette Fusion Razor', 250.00, 30, 4),
-- Cleaning Supplies (5)
('Ariel Powder Detergent 2kg', 195.00, 50, 5),
('Surf Powder Detergent 1kg', 88.00, 75, 5),
('Zonrox Bleach 1L', 48.00, 80, 5),
('Joy Dishwashing Liquid 250ml', 55.00, 90, 5),
-- Condiments & Sauces (6)
('UFC Banana Ketchup 550g', 68.00, 100, 6),
('Silver Swan Soy Sauce 1L', 72.00, 95, 6),
('Datu Puti Vinegar 1L', 38.00, 110, 6),
('Knorr Liquid Seasoning 130ml', 45.00, 120, 6),
('Mang Tomas All-Purpose Sauce 550g', 70.00, 85, 6),
-- Instant Noodles & Pasta (7)
('Lucky Me Pancit Canton Original 80g', 16.00, 400, 7),
('Nissin Cup Noodles Chicken 60g', 22.00, 300, 7),
('Payless Spaghetti 400g', 45.00, 120, 7),
('Del Monte Spaghetti Sauce Sweet Style 250g', 55.00, 100, 7),
-- Dairy & Eggs (8)
('Alaska Evaporated Milk 370ml', 38.00, 130, 8),
('Bear Brand Adult Plus 300g', 145.00, 70, 8),
('Nestle All Purpose Cream 250ml', 55.00, 90, 8),
-- Frozen Foods (9)
('San Miguel Chicken Nuggets 400g', 155.00, 45, 9),
('Purefoods Tender Juicy Hotdog 500g', 135.00, 55, 9),
('Magnolia Chicken 1kg', 175.00, 40, 9),
-- Rice & Grains (10)
('Sinandomeng Premium Rice 5kg', 280.00, 80, 10),
('Dinorado Rice 5kg', 310.00, 65, 10),
('Mindanao Red Rice 1kg', 75.00, 50, 10);

-- =============================================
-- SHIPMENTS (restocking from suppliers)
-- =============================================
INSERT INTO SHIPMENT (supplier_id, shipment_date, status, reference_number) VALUES
(1, '2025-10-01', 'DELIVERED', 'SHP-2025-0001'),
(2, '2025-10-03', 'DELIVERED', 'SHP-2025-0002'),
(3, '2025-10-07', 'DELIVERED', 'SHP-2025-0003'),
(4, '2025-10-10', 'DELIVERED', 'SHP-2025-0004'),
(5, '2025-10-15', 'DELIVERED', 'SHP-2025-0005'),
(6, '2025-10-18', 'DELIVERED', 'SHP-2025-0006'),
(7, '2025-11-02', 'DELIVERED', 'SHP-2025-0007'),
(8, '2025-11-05', 'DELIVERED', 'SHP-2025-0008'),
(9, '2025-11-10', 'DELIVERED', 'SHP-2025-0009'),
(10, '2025-11-14', 'DELIVERED', 'SHP-2025-0010'),
(1, '2025-11-20', 'DELIVERED', 'SHP-2025-0011'),
(2, '2025-11-25', 'DELIVERED', 'SHP-2025-0012'),
(3, '2025-12-01', 'SHIPPED', 'SHP-2025-0013'),
(4, '2025-12-05', 'PENDING', 'SHP-2025-0014'),
(5, '2025-12-08', 'PENDING', 'SHP-2025-0015');

-- =============================================
-- SHIPMENT ITEMS
-- =============================================
INSERT INTO SHIPMENT_ITEM (shipment_id, product_id, quantity, unit_cost) VALUES
-- SHP-0001 (Monde Nissin - noodles/snacks)
(1, 33, 500, 11.00),
(1, 34, 300, 16.00),
(1, 12, 400, 6.50),
-- SHP-0002 (URC - snacks)
(2, 8, 200, 22.00),
(2, 9, 200, 25.00),
(2, 11, 300, 20.00),
-- SHP-0003 (San Miguel - beverages)
(3, 1, 300, 40.00),
(3, 6, 250, 38.00),
-- SHP-0004 (Nestlé - dairy/beverages)
(4, 37, 200, 32.00),
(4, 38, 150, 95.00),
(4, 39, 200, 38.00),
-- SHP-0005 (Century Pacific - canned goods)
(5, 14, 500, 27.00),
(5, 15, 300, 55.00),
-- SHP-0006 (Del Monte - canned/condiments)
(6, 17, 400, 24.00),
(6, 28, 300, 42.00),
(6, 35, 250, 36.00),
-- SHP-0007 (Unilever - personal care/cleaning)
(7, 19, 150, 75.00),
(7, 22, 100, 115.00),
(7, 24, 200, 120.00),
(7, 25, 150, 58.00),
-- SHP-0008 (Alaska - dairy)
(8, 37, 300, 24.00),
(8, 38, 100, 92.00),
-- SHP-0009 (Rebisco - snacks)
(9, 12, 600, 6.00),
(9, 13, 200, 38.00),
-- SHP-0010 (Fly Ace - rice)
(10, 42, 200, 190.00),
(10, 43, 150, 210.00),
(10, 44, 120, 52.00),
-- SHP-0011 (Monde Nissin - restock)
(11, 33, 600, 11.00),
(11, 34, 400, 15.50),
-- SHP-0012 (URC - restock)
(12, 8, 300, 22.00),
(12, 10, 400, 17.50),
-- SHP-0013 (San Miguel - in transit)
(13, 40, 100, 100.00),
(13, 41, 120, 90.00),
-- SHP-0014 (Nestlé - pending)
(14, 4, 300, 16.00),
(14, 3, 300, 18.00),
-- SHP-0015 (Century Pacific - pending)
(15, 16, 500, 15.00),
(15, 18, 300, 19.00);

-- =============================================
-- ORDERS
-- =============================================
INSERT INTO ORDERS (customer_id, order_date, status, total_price, order_type) VALUES
(1,  '2025-10-05', 'DELIVERED', 283.00, 'IN_STORE'),
(2,  '2025-10-06', 'DELIVERED', 520.00, 'DELIVERY'),
(3,  '2025-10-08', 'DELIVERED', 175.00, 'IN_STORE'),
(4,  '2025-10-09', 'DELIVERED', 410.00, 'DELIVERY'),
(5,  '2025-10-11', 'DELIVERED', 248.00, 'IN_STORE'),
(6,  '2025-10-12', 'DELIVERED', 630.00, 'DELIVERY'),
(7,  '2025-10-14', 'DELIVERED', 156.00, 'IN_STORE'),
(8,  '2025-10-16', 'DELIVERED', 345.00, 'DELIVERY'),
(9,  '2025-10-18', 'DELIVERED', 192.00, 'IN_STORE'),
(10, '2025-10-20', 'DELIVERED', 770.00, 'DELIVERY'),
(11, '2025-10-22', 'DELIVERED', 224.00, 'IN_STORE'),
(12, '2025-10-23', 'DELIVERED', 488.00, 'DELIVERY'),
(13, '2025-10-25', 'DELIVERED', 310.00, 'IN_STORE'),
(14, '2025-10-27', 'DELIVERED', 555.00, 'DELIVERY'),
(15, '2025-10-29', 'DELIVERED', 138.00, 'IN_STORE'),
(16, '2025-11-01', 'DELIVERED', 695.00, 'DELIVERY'),
(17, '2025-11-03', 'DELIVERED', 264.00, 'IN_STORE'),
(18, '2025-11-05', 'DELIVERED', 420.00, 'DELIVERY'),
(19, '2025-11-07', 'DELIVERED', 189.00, 'IN_STORE'),
(20, '2025-11-09', 'DELIVERED', 815.00, 'DELIVERY'),
(1,  '2025-11-11', 'DELIVERED', 350.00, 'IN_STORE'),
(3,  '2025-11-12', 'DELIVERED', 475.00, 'DELIVERY'),
(5,  '2025-11-14', 'DELIVERED', 222.00, 'IN_STORE'),
(7,  '2025-11-15', 'DELIVERED', 540.00, 'DELIVERY'),
(9,  '2025-11-17', 'DELIVERED', 168.00, 'IN_STORE'),
(21, '2025-11-19', 'SHIPPED', 390.00, 'DELIVERY'),
(22, '2025-11-20', 'DELIVERED', 245.00, 'IN_STORE'),
(23, '2025-11-22', 'SHIPPED', 615.00, 'DELIVERY'),
(24, '2025-11-24', 'DELIVERED', 178.00, 'IN_STORE'),
(25, '2025-11-25', 'SHIPPED', 430.00, 'DELIVERY'),
(2,  '2025-11-27', 'DELIVERED', 310.00, 'IN_STORE'),
(4,  '2025-11-28', 'PENDING', 560.00, 'DELIVERY'),
(6,  '2025-11-29', 'DELIVERED', 195.00, 'IN_STORE'),
(8,  '2025-11-30', 'PENDING', 720.00, 'DELIVERY'),
(10, '2025-12-01', 'DELIVERED', 285.00, 'IN_STORE'),
(11, '2025-12-02', 'PENDING', 490.00, 'DELIVERY'),
(12, '2025-12-03', 'DELIVERED', 160.00, 'IN_STORE'),
(13, '2025-12-04', 'PENDING', 875.00, 'DELIVERY'),
(14, '2025-12-05', 'DELIVERED', 225.00, 'IN_STORE'),
(15, '2025-12-05', 'CANCELLED', 340.00, 'DELIVERY'),
(16, '2025-12-06', 'PENDING', 415.00, 'IN_STORE');

-- =============================================
-- IN_STORE_ORDER (order_type = 'IN_STORE')
-- order_ids: 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41
-- =============================================
INSERT INTO IN_STORE_ORDER (order_id, release_time, claimed_by) VALUES
(1,  '09:15:00', 'Maria Santos'),
(3,  '10:30:00', 'Ana Cruz'),
(5,  '11:00:00', 'Liza Mendoza'),
(7,  '14:45:00', 'Cristina Bautista'),
(9,  '08:50:00', 'Rosa Aquino'),
(11, '15:20:00', 'Marites Gonzales'),
(13, '10:05:00', 'Nelia Ramos'),
(15, '13:30:00', 'Teresita Navarro'),
(17, '09:45:00', 'Gloria Padilla'),
(19, '11:55:00', 'Rosario Mercado'),
(21, '10:10:00', 'Maria Santos'),
(23, '14:00:00', 'Ana Cruz'),
(25, '09:30:00', 'Rosa Aquino'),
(27, '16:15:00', 'Alfredo Jimenez'),
(29, '11:40:00', 'Jose Reyes'),
(31, '08:30:00', 'Ramon Villanueva'),
(33, '12:00:00', 'Cristina Bautista'),
(35, '10:50:00', 'Felix Soriano'),
(37, '15:00:00', 'Shirley Ramirez'),
(39, '09:00:00', 'Arnold Castillo'),
(41, '13:20:00', NULL);

-- =============================================
-- DELIVERY_ORDER (order_type = 'DELIVERY')
-- order_ids: 2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40
-- =============================================
INSERT INTO DELIVERY_ORDER (order_id, delivery_note) VALUES
(2,  'Leave at the gate'),
(4,  'Call before delivery'),
(6,  'Fragile items, handle with care'),
(8,  NULL),
(10, 'Ring the doorbell twice'),
(12, 'Give to guard if not home'),
(14, 'Deliver after 5PM'),
(16, NULL),
(18, 'Place inside the barangay hall'),
(20, 'Call upon arrival'),
(22, NULL),
(24, 'Pack items separately'),
(26, 'Leave with neighbor if absent'),
(28, NULL),
(30, 'Handle items carefully'),
(32, 'Deliver in the morning'),
(34, 'Deliver between 2-4PM'),
(36, 'Leave at reception'),
(38, 'Fragile - egg included'),
(40, NULL);

-- =============================================
-- DELIVERY (for DELIVERY orders)
-- =============================================
INSERT INTO DELIVERY (order_id, delivery_date, delivery_street, delivery_barangay, delivery_city, delivery_province, delivered_by, status) VALUES
(2,  '2025-10-07', '45 Mabini Ave',        'Bagumbayan',    'Legazpi City', 'Albay', 'Mark Villanueva', 'DELIVERED'),
(4,  '2025-10-10', '88 Quezon Blvd',       'Cabangan',      'Legazpi City', 'Albay', 'Rey Castillo',    'DELIVERED'),
(6,  '2025-10-13', '55 Magsaysay Ave',     'Rawis',         'Legazpi City', 'Albay', 'Mark Villanueva', 'DELIVERED'),
(8,  '2025-10-17', '9 Luna St',            'Bigaa',         'Legazpi City', 'Albay', 'Jun Macaraeg',    'DELIVERED'),
(10, '2025-10-21', '66 Burgos St',         'Taysan',        'Legazpi City', 'Albay', 'Rey Castillo',    'DELIVERED'),
(12, '2025-10-24', '17 Osmeña St',         'Buyuan',        'Legazpi City', 'Albay', 'Mark Villanueva', 'DELIVERED'),
(14, '2025-10-28', '90 Roxas Blvd',        'Estanza',       'Legazpi City', 'Albay', 'Jun Macaraeg',    'DELIVERED'),
(16, '2025-11-02', '11 Dimaporo St',       'Banquerohan',   'Legazpi City', 'Albay', 'Rey Castillo',    'DELIVERED'),
(18, '2025-11-06', '44 Katipunan St',      'Bonot',         'Legazpi City', 'Albay', 'Mark Villanueva', 'DELIVERED'),
(20, '2025-11-10', '77 Gen. Luna St',      'Dita',          'Legazpi City', 'Albay', 'Jun Macaraeg',    'DELIVERED'),
(22, '2025-11-13', '7 Bonifacio St',       'Puro',          'Legazpi City', 'Albay', 'Rey Castillo',    'DELIVERED'),
(24, '2025-11-16', '21 Del Pilar St',      'Pinaric',       'Legazpi City', 'Albay', 'Mark Villanueva', 'DELIVERED'),
(26, '2025-11-20', '20 Mabini St',         'Gogon',         'Legazpi City', 'Albay', 'Jun Macaraeg',    'SHIPPED'),
(28, '2025-11-23', '2 National Highway',   'Landco',        'Legazpi City', 'Albay', 'Rey Castillo',    'SHIPPED'),
(30, '2025-11-26', '16 Mabini Extension',  'San Joaquin',   'Legazpi City', 'Albay', 'Mark Villanueva', 'SHIPPED'),
(32, '2025-11-29', '88 Quezon Blvd',       'Cabangan',      'Legazpi City', 'Albay', 'Jun Macaraeg',    'PENDING'),
(34, '2025-12-02', '9 Luna St',            'Bigaa',         'Legazpi City', 'Albay', 'Rey Castillo',    'PENDING'),
(36, '2025-12-04', '44 Katipunan St',      'Bonot',         'Legazpi City', 'Albay', 'Mark Villanueva', 'PENDING'),
(38, '2025-12-06', '90 Roxas Blvd',        'Estanza',       'Legazpi City', 'Albay', 'Jun Macaraeg',    'PENDING'),
(40, '2025-12-06', '28 Ocampo St',         'Homapon',       'Legazpi City', 'Albay', NULL,              'CANCELLED');

-- =============================================
-- ORDER ITEMS
-- =============================================
INSERT INTO ORDER_ITEM (order_id, product_id, quantity, selling_price) VALUES
-- Order 1 (in-store, Maria Santos)
(1, 33, 3, 16.00), (1, 14, 2, 42.00), (1, 1, 1, 65.00), (1, 12, 5, 10.00),
-- Order 2 (delivery, Jose Reyes)
(2, 42, 1, 280.00), (2, 15, 2, 85.00), (2, 29, 1, 68.00),
-- Order 3 (in-store, Ana Cruz)
(3, 33, 4, 16.00), (3, 16, 3, 24.00),
-- Order 4 (delivery, Carlo Dela Cruz)
(4, 43, 1, 310.00), (4, 14, 2, 42.00), (4, 30, 1, 72.00),
-- Order 5 (in-store, Liza Mendoza)
(5, 1, 2, 65.00), (5, 8, 1, 35.00), (5, 12, 3, 10.00),
-- Order 6 (delivery, Ramon Villanueva)
(6, 42, 2, 280.00), (6, 15, 1, 85.00),
-- Order 7 (in-store, Cristina Bautista)
(7, 33, 3, 16.00), (7, 4, 2, 25.00), (7, 12, 3, 10.00),
-- Order 8 (delivery, Eduardo Torres)
(8, 19, 1, 115.00), (8, 20, 1, 42.00), (8, 21, 1, 72.00), (8, 25, 1, 88.00),
-- Order 9 (in-store, Rosa Aquino)
(9, 33, 4, 16.00), (9, 16, 3, 24.00),
-- Order 10 (delivery, Felix Soriano)
(10, 42, 2, 280.00), (10, 43, 1, 310.00),
-- Order 11 (in-store, Marites Gonzales)
(11, 14, 2, 42.00), (11, 16, 3, 24.00), (11, 31, 2, 38.00),
-- Order 12 (delivery, Dante Ferrer)
(12, 1, 2, 65.00), (12, 6, 2, 62.00), (12, 9, 3, 38.00), (12, 11, 2, 32.00),
-- Order 13 (in-store, Nelia Ramos)
(13, 33, 5, 16.00), (13, 3, 3, 28.00), (13, 18, 2, 30.00),
-- Order 14 (delivery, Arnold Castillo)
(14, 38, 2, 145.00), (14, 15, 2, 85.00), (14, 32, 3, 45.00),
-- Order 15 (in-store, Teresita Navarro)
(15, 33, 3, 16.00), (15, 4, 2, 25.00),
-- Order 16 (delivery, Rodrigo Lim)
(16, 42, 2, 280.00), (16, 22, 1, 72.00), (16, 21, 1, 72.00),
-- Order 17 (in-store, Gloria Padilla)
(17, 14, 3, 42.00), (17, 16, 4, 24.00),
-- Order 18 (delivery, Benjamin Uy)
(18, 9, 3, 38.00), (18, 8, 3, 35.00), (18, 11, 2, 32.00), (18, 10, 2, 28.00),
-- Order 19 (in-store, Rosario Mercado)
(19, 33, 3, 16.00), (19, 12, 5, 10.00), (19, 4, 2, 25.00),
-- Order 20 (delivery, Dennis Tan)
(20, 43, 1, 310.00), (20, 41, 1, 135.00), (20, 40, 1, 155.00), (20, 39, 2, 55.00),
-- Order 21 (in-store, Maria Santos repeat)
(21, 14, 3, 42.00), (21, 15, 1, 85.00), (21, 1, 1, 65.00),
-- Order 22 (delivery, Ana Cruz repeat)
(22, 42, 1, 280.00), (22, 33, 5, 16.00), (22, 19, 1, 115.00),
-- Order 23 (in-store, Liza Mendoza repeat)
(23, 33, 5, 16.00), (23, 4, 3, 25.00),
-- Order 24 (delivery, Cristina Bautista repeat)
(24, 38, 2, 145.00), (24, 15, 2, 85.00), (24, 28, 2, 68.00),
-- Order 25 (in-store, Rosa Aquino repeat)
(25, 12, 5, 10.00), (25, 16, 3, 24.00),
-- Order 26 (delivery, Shirley Ramirez)
(26, 42, 1, 280.00), (26, 14, 2, 42.00), (26, 3, 2, 28.00),
-- Order 27 (in-store, Alfredo Jimenez)
(27, 33, 4, 16.00), (27, 15, 1, 85.00), (27, 12, 3, 10.00),
-- Order 28 (delivery, Concepcion Flores)
(28, 43, 1, 310.00), (28, 19, 1, 115.00), (28, 24, 1, 88.00),
-- Order 29 (in-store, Victor Pascual)
(29, 14, 2, 42.00), (29, 16, 3, 24.00),
-- Order 30 (delivery, Imelda Aguilar)
(30, 42, 1, 280.00), (30, 33, 5, 16.00), (30, 7, 3, 22.00),
-- Order 31 (in-store, Jose Reyes repeat)
(31, 1, 2, 65.00), (31, 15, 1, 85.00), (31, 33, 3, 16.00),
-- Order 32 (delivery, Carlo Dela Cruz repeat)
(32, 43, 1, 310.00), (32, 40, 1, 155.00), (32, 14, 2, 42.00),
-- Order 33 (in-store, Ramon Villanueva repeat)
(33, 33, 5, 16.00), (33, 4, 3, 25.00),
-- Order 34 (delivery, Eduardo Torres repeat)
(34, 42, 2, 280.00), (34, 16, 2, 24.00), (34, 15, 1, 85.00),
-- Order 35 (in-store, Felix Soriano repeat)
(35, 14, 3, 42.00), (35, 33, 3, 16.00),
-- Order 36 (delivery, Marites Gonzales repeat)
(36, 38, 2, 145.00), (36, 15, 2, 85.00), (36, 21, 1, 72.00),
-- Order 37 (in-store, Dante Ferrer repeat)
(37, 33, 4, 16.00), (37, 12, 5, 10.00),
-- Order 38 (delivery, Nelia Ramos repeat)
(38, 41, 3, 135.00), (38, 43, 1, 310.00), (38, 37, 2, 38.00),
-- Order 39 (in-store, Arnold Castillo repeat)
(39, 14, 2, 42.00), (39, 16, 3, 24.00), (39, 1, 1, 65.00),
-- Order 40 (delivery - cancelled, Teresita Navarro)
(40, 42, 1, 280.00), (40, 14, 1, 42.00),
-- Order 41 (in-store, Rodrigo Lim)
(41, 14, 3, 42.00), (41, 33, 5, 16.00), (41, 4, 3, 25.00);