-- Get all shipments with supplier name
SELECT s.shipment_id, s.reference_number, s.shipment_date,
       s.status, sup.supplier_name
FROM SHIPMENT s
JOIN SUPPLIER sup ON s.supplier_id = sup.supplier_id
ORDER BY s.shipment_date DESC;

-- Get all shipment items for a specific shipment
SELECT si.shipment_item_id, p.product_name,
       si.quantity, si.unit_cost,
       (si.quantity * si.unit_cost) AS total_cost
FROM SHIPMENT_ITEM si
JOIN PRODUCT p ON si.product_id = p.product_id
WHERE si.shipment_id = 1;

-- Update shipment status
UPDATE SHIPMENT
SET status = 'DELIVERED'
WHERE shipment_id = 1;