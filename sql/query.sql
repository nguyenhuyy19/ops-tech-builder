
--This is a sample data for reference to meet the criteria for writing SQL Query

DROP TABLE IF EXISTS invoices;
CREATE TABLE invoices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vendor VARCHAR(100),
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    created_at DATETIME
);
INSERT INTO invoices (id, vendor, amount, status, created_at) VALUES
(1, 'Vendor A', 1500.00, 'paid', NOW() - INTERVAL 5 DAY),
(2, 'Vendor A', 2500.00, 'paid', NOW() - INTERVAL 10 DAY),
(3, 'Vendor B', 3000.00, 'paid', NOW() - INTERVAL 2 DAY),
(4, 'Vendor C', 1800.00, 'paid', NOW() - INTERVAL 15 DAY),
(5, 'Vendor D', 2200.00, 'paid', NOW() - INTERVAL 20 DAY),
(6, 'Vendor E', 1000.00, 'paid', NOW() - INTERVAL 1 DAY),
(7, 'Vendor F', 500.00, 'paid', NOW() - INTERVAL 3 DAY);

INSERT INTO invoices (id, vendor, amount, status, created_at) VALUES
(8, 'Vendor A', 999.00, 'unpaid', NOW() - INTERVAL 5 DAY),
(9, 'Vendor B', 888.00, 'pending', NOW() - INTERVAL 8 DAY),
(10, 'Vendor C', 2000.00, 'paid', NOW() - INTERVAL 45 DAY),
(11, 'Vendor D', 1300.00, 'unpaid', NOW() - INTERVAL 60 DAY);


-- SQL Query 

SELECT 
    vendor,
    SUM(amount) AS total_amount
FROM 
    invoices
WHERE 
    status = 'paid'
    AND created_at >= NOW() - INTERVAL 30 DAY
GROUP BY 
    vendor
ORDER BY 
    total_amount DESC
LIMIT 5;
