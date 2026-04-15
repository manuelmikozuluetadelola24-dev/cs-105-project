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
UPDATE PRODUCT
SET stock_quantity = stock_quantity - ORDER_ITEM.quantity
WHERE PRODUCT.product_id = ORDER_ITEM.product_id;

-- Update order status
UPDATE ORDERS
SET status = 'DELIVERED'
WHERE order_id = 1;
