-- View all orders with customer info
SELECT o.order_id, c.customer_name, o.order_date,
       o.order_type, o.status, o.total_price
FROM ORDERS o
JOIN CUSTOMER c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;

-- View items in a specific order
SELECT oi.order_item_id, p.product_name,
       oi.quantity, oi.selling_price,
       (oi.quantity * oi.selling_price) AS item_total
FROM ORDER_ITEM oi
JOIN PRODUCT p ON oi.product_id = p.product_id
WHERE oi.order_id = 1;

-- Deduct stock when an order item is placed
<<<<<<< HEAD:order_processing.sql
UPDATE PRODUCT
SET stock_quantity = stock_quantity - ORDER_ITEM.quantity
WHERE PRODUCT.product_id = ORDER_ITEM.product_id;
=======
UPDATE PRODUCT, ORDER_ITEM
SET stock_quantity = stock_quantity - ORDER_ITEM.quantity
WHERE ORDER_ITEM.product_id = PRODUCT.product_id
AND ORDER_ITEM.order_item_id = (SELECT order_item_id FROM ORDER_ITEM ORDER BY order_item_id DESC LIMIT 1);
>>>>>>> 03857d35ffe3c664a6c4ea2d48727434113d4a8d:Features/order_processing.sql

-- Update order status
UPDATE ORDERS
SET status = 'DELIVERED'
WHERE order_id = 1;
