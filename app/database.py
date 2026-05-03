import sqlite3

conn = sqlite3.connect("delola_store.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS SUPPLIER (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    contact_number TEXT,
    address TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PRODUCT_CATEGORY (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PRODUCT (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category_id INTEGER,
    price REAL NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES PRODUCT_CATEGORY(category_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS CUSTOMER (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    contact_number TEXT,
    customer_city TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS SHIPMENT (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    reference_number TEXT,
    shipment_date TEXT,
    status TEXT DEFAULT 'PENDING',
    FOREIGN KEY (supplier_id) REFERENCES SUPPLIER(supplier_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS SHIPMENT_ITEM (
    shipment_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_cost REAL,
    FOREIGN KEY (shipment_id) REFERENCES SHIPMENT(shipment_id),
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ORDERS (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    order_type TEXT,
    status TEXT DEFAULT 'PENDING',
    total_price REAL,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ORDER_ITEM (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    selling_price REAL,
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id),
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS DELIVERY (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    delivery_date TEXT,
    status TEXT DEFAULT 'PENDING',
    delivered_by TEXT,
    delivery_street TEXT,
    delivery_barangay TEXT,
    delivery_city TEXT,
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully.")