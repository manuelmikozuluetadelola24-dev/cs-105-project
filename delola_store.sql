CREATE TABLE IF NOT EXISTS PRODUCT_CATEGORY (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS CUSTOMER (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    customer_street VARCHAR(255) NOT NULL,
    customer_barangay VARCHAR(255) NOT NULL,
    customer_city VARCHAR(255) NOT NULL,
    customer_province VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS SUPPLIER (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    supplier_street VARCHAR(255) NOT NULL,
    supplier_barangay VARCHAR(255) NOT NULL,
    supplier_city VARCHAR(255) NOT NULL,
    supplier_province VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS PRODUCT (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES PRODUCT_CATEGORY(category_id)
);

CREATE TABLE IF NOT EXISTS ORDERS (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATE NOT NULL,
    status ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED') DEFAULT 'PENDING',
    total_price DECIMAL(10, 2) NOT NULL,
    order_type ENUM('IN_STORE', 'DELIVERY') NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    UNIQUE (customer_id, order_date, order_type)
);

CREATE TABLE IF NOT EXISTS ORDER_ITEM (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    selling_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id),
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

-- Subtype tables for different order types
CREATE TABLE IF NOT EXISTS IN_STORE_ORDER (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    release_time TIME NULL,
    claimed_by VARCHAR(255) NULL,
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

CREATE TABLE IF NOT EXISTS DELIVERY_ORDER (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    delivery_note VARCHAR(255) NULL,
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

CREATE TABLE IF NOT EXISTS DELIVERY (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    delivery_date DATE NOT NULL,
    delivery_street VARCHAR(255) NOT NULL,
    delivery_barangay VARCHAR(255) NOT NULL,
    delivery_city VARCHAR(255) NOT NULL,
    delivery_province VARCHAR(255) NOT NULL,
    delivered_by VARCHAR(255),
    status ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED') DEFAULT 'PENDING',
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

CREATE TABLE IF NOT EXISTS SHIPMENT (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    shipment_date DATE NOT NULL,
    status ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED') DEFAULT 'PENDING',
    reference_number VARCHAR(255) NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES SUPPLIER(supplier_id)
);

CREATE TABLE IF NOT EXISTS SHIPMENT_ITEM (
    shipment_item_id INT AUTO_INCREMENT PRIMARY KEY,
    shipment_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (shipment_id) REFERENCES SHIPMENT(shipment_id),
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)
);

CREATE TABLE IF NOT EXISTS delola_store.`users` (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('OWNER', 'EMPLOYEE') NOT NULL DEFAULT 'EMPLOYEE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (username)
);

-- Insert default users
INSERT IGNORE INTO delola_store.users (username, password, role) VALUES ('ace', 'ace123', 'OWNER');
INSERT IGNORE INTO delola_store.users (username, password, role) VALUES ('miko', 'miko123', 'OWNER');
INSERT IGNORE INTO delola_store.users (username, password, role) VALUES ('mel', 'mel123', 'OWNER');
INSERT IGNORE INTO delola_store.users (username, password, role) VALUES ('steph', 'steph123', 'OWNER');
INSERT IGNORE INTO delola_store.users (username, password, role) VALUES ('emp', 'emp123', 'EMPLOYEE');