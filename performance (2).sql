

USE gated_community_db;



EXPLAIN ANALYZE
SELECT v.name AS visitor_name, al.entry_time, al.exit_time, u.unit_number
FROM access_logs al
JOIN visitors v ON al.visitor_id = v.id
JOIN units u ON al.unit_id = u.id
WHERE u.unit_number = '101'
ORDER BY al.entry_time DESC;



EXPLAIN ANALYZE
SELECT payment_type, SUM(amount) AS total_revenue
FROM payments
WHERE status = 'Paid'
GROUP BY payment_type;






EXPLAIN ANALYZE
SELECT u.unit_number, us.username, SUM(p.amount) AS outstanding_amount
FROM residents r
JOIN units u ON r.unit_id = u.id
JOIN users us ON r.user_id = us.id
JOIN payments p ON r.id = p.resident_id
WHERE p.status = 'Overdue'
GROUP BY u.unit_number, us.username
HAVING outstanding_amount > 500
ORDER BY outstanding_amount DESC;

