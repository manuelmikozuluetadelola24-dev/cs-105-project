-- Filter products by category
SELECT p.product_id, p.product_name,
       p.price, p.stock_quantity
FROM PRODUCT p
JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
WHERE pc.category_name = 'Beverages';

-- Sort customers alphabetically (descending)
SELECT customer_id, customer_name,
       customer_city, contact_number
FROM CUSTOMER
ORDER BY customer_name DESC;