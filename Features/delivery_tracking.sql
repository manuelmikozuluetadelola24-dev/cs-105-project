-- View all deliveries with customer and order info
SELECT d.delivery_id, c.customer_name, o.order_id,
       d.delivery_date, d.status, d.delivered_by,
       CONCAT(d.delivery_street, ', ', d.delivery_barangay,
              ', ', d.delivery_city) AS delivery_address
FROM DELIVERY d
JOIN ORDERS o ON d.order_id = o.order_id
JOIN CUSTOMER c ON o.customer_id = c.customer_id
ORDER BY d.delivery_date DESC;

-- Filter deliveries by status
SELECT d.delivery_id, c.customer_name,
       d.delivery_date, d.status, d.delivered_by
FROM DELIVERY d
JOIN ORDERS o ON d.order_id = o.order_id
JOIN CUSTOMER c ON o.customer_id = c.customer_id
WHERE d.status = 'PENDING';