-- View current stock levels per product
SELECT p.product_id, p.product_name,
       pc.category_name, p.stock_quantity, p.price
FROM PRODUCT p
JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
ORDER BY p.stock_quantity ASC;

-- Update stock when shipment is received (run per item)
UPDATE PRODUCT p
JOIN SHIPMENT_ITEM si ON p.product_id = si.product_id
SET p.stock_quantity = p.stock_quantity + si.quantity
WHERE si.shipment_id = 1;

-- Low stock alert (threshold: 10 units)
SELECT p.product_id, p.product_name,
       pc.category_name, p.stock_quantity
FROM PRODUCT p
JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
WHERE p.stock_quantity <= 10
ORDER BY p.stock_quantity ASC;