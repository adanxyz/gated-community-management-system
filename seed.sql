

USE gated_community_db;


SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE complaints;
TRUNCATE TABLE payments;
TRUNCATE TABLE bookings;
TRUNCATE TABLE amenities;
TRUNCATE TABLE access_logs;
TRUNCATE TABLE visitors;
TRUNCATE TABLE residents;
TRUNCATE TABLE units;
TRUNCATE TABLE users;
TRUNCATE TABLE staff;
TRUNCATE TABLE roles;
SET FOREIGN_KEY_CHECKS = 1;


INSERT INTO roles (role_name, description) VALUES
('Admin', 'Full system access'),
('Resident', 'Access to own unit and community services'),
('Security', 'Manage visitors and logs'),
('Maintenance', 'Manage complaints and repairs'),
('Manager', 'Oversee community operations');


INSERT INTO users (username, password_hash, email, phone, role_id) VALUES
('admin01', 'h_admin', 'admin@community.com', '555-0101', 1),
('john_doe', 'h_john', 'john.doe@email.com', '555-0201', 2),
('jane_smith', 'h_jane', 'jane@email.com', '555-0202', 2),
('alice_w', 'h_alice', 'alice@email.com', '555-0203', 2),
('bob_b', 'h_bob', 'bob@email.com', '555-0204', 2),
('charlie_d', 'h_charlie', 'charlie@email.com', '555-0205', 2),

('res001', 'h_res', 'res001@email.com', '555-1001', 2), ('res002', 'h_res', 'res002@email.com', '555-1002', 2),
('res003', 'h_res', 'res003@email.com', '555-1003', 2), ('res004', 'h_res', 'res004@email.com', '555-1004', 2),
('res005', 'h_res', 'res005@email.com', '555-1005', 2), ('res006', 'h_res', 'res006@email.com', '555-1006', 2),
('res007', 'h_res', 'res007@email.com', '555-1007', 2), ('res008', 'h_res', 'res008@email.com', '555-1008', 2),
('res009', 'h_res', 'res009@email.com', '555-1009', 2), ('res010', 'h_res', 'res010@email.com', '555-1010', 2),
('res011', 'h_res', 'res011@email.com', '555-1011', 2), ('res012', 'h_res', 'res012@email.com', '555-1012', 2),
('res013', 'h_res', 'res013@email.com', '555-1013', 2), ('res014', 'h_res', 'res014@email.com', '555-1014', 2),
('res015', 'h_res', 'res015@email.com', '555-1015', 2), ('res016', 'h_res', 'res016@email.com', '555-1016', 2),
('res017', 'h_res', 'res017@email.com', '555-1017', 2), ('res018', 'h_res', 'res018@email.com', '555-1018', 2),
('res019', 'h_res', 'res019@email.com', '555-1019', 2), ('res020', 'h_res', 'res020@email.com', '555-1020', 2),
('res021', 'h_res', 'res021@email.com', '555-1021', 2), ('res022', 'h_res', 'res022@email.com', '555-1022', 2),
('res023', 'h_res', 'res023@email.com', '555-1023', 2), ('res024', 'h_res', 'res024@email.com', '555-1024', 2),
('res025', 'h_res', 'res025@email.com', '555-1025', 2), ('res026', 'h_res', 'res026@email.com', '555-1026', 2),
('res027', 'h_res', 'res027@email.com', '555-1027', 2), ('res028', 'h_res', 'res028@email.com', '555-1028', 2),
('res029', 'h_res', 'res029@email.com', '555-1029', 2), ('res030', 'h_res', 'res030@email.com', '555-1030', 2),
('guard01', 'h_guard', 'guard01@security.com', '555-0301', 3), ('guard02', 'h_guard', 'guard02@security.com', '555-0302', 3),
('maint01', 'h_maint', 'maint01@maint.com', '555-0401', 4), ('manager01', 'h_mgr', 'manager01@comm.com', '555-0501', 5);


INSERT INTO units (unit_number, block, unit_type, square_feet) VALUES
('101', 'A', '1BHK', 800), ('102', 'A', '1BHK', 800), ('103', 'A', '2BHK', 1200), ('104', 'A', '2BHK', 1200), ('105', 'A', '3BHK', 1800),
('201', 'B', '1BHK', 850), ('202', 'B', '1BHK', 850), ('203', 'B', '2BHK', 1250), ('204', 'B', '2BHK', 1250), ('205', 'B', '3BHK', 1900),
('301', 'C', '1BHK', 800), ('302', 'C', '1BHK', 800), ('303', 'C', '2BHK', 1200), ('304', 'C', '2BHK', 1200), ('305', 'C', 'Villa', 2500),
('401', 'D', '2BHK', 1300), ('402', 'D', '2BHK', 1300), ('403', 'D', '3BHK', 1850), ('404', 'D', '3BHK', 1850), ('405', 'D', 'Villa', 3000),

('501', 'E', '1BHK', 800), ('502', 'E', '1BHK', 800), ('503', 'E', '2BHK', 1200), ('504', 'E', '2BHK', 1200), ('505', 'E', '3BHK', 1800),
('601', 'F', '1BHK', 850), ('602', 'F', '1BHK', 850), ('603', 'F', '2BHK', 1250), ('604', 'F', '2BHK', 1250), ('605', 'F', '3BHK', 1900),
('701', 'G', '1BHK', 800), ('702', 'G', '1BHK', 800), ('703', 'G', '2BHK', 1200), ('704', 'G', '2BHK', 1200), ('705', 'G', 'Villa', 2500),
('801', 'H', '2BHK', 1300), ('802', 'H', '2BHK', 1300), ('803', 'H', '3BHK', 1850), ('804', 'H', '3BHK', 1850), ('805', 'H', 'Villa', 3000),
('901', 'I', '1BHK', 800), ('902', 'I', '1BHK', 800), ('903', 'I', '2BHK', 1200), ('904', 'I', '2BHK', 1200), ('905', 'I', '3BHK', 1800),
('1001', 'J', '1BHK', 850), ('1002', 'J', '1BHK', 850), ('1003', 'J', '2BHK', 1250), ('1004', 'J', '2BHK', 1250), ('1005', 'J', '3BHK', 1900);


INSERT INTO residents (user_id, unit_id, residency_status, move_in_date) VALUES
(2, 1, 'Owner', '2023-01-01'), (3, 2, 'Tenant', '2023-02-01'), (4, 3, 'Owner', '2023-03-01'), (5, 4, 'Owner', '2023-04-01'), (6, 5, 'Tenant', '2023-05-01'),
(7, 6, 'Owner', '2023-06-01'), (8, 7, 'Owner', '2023-07-01'), (9, 8, 'Tenant', '2023-08-01'), (10, 9, 'Owner', '2023-09-01'), (11, 10, 'Owner', '2023-10-01'),
(12, 11, 'Tenant', '2023-11-01'), (13, 12, 'Owner', '2023-12-01'), (14, 13, 'Owner', '2024-01-01'), (15, 14, 'Tenant', '2024-02-01'), (16, 15, 'Owner', '2024-03-01'),
(17, 16, 'Owner', '2024-04-01'), (18, 17, 'Tenant', '2024-05-01'), (19, 18, 'Owner', '2024-06-01'), (20, 19, 'Owner', '2024-07-01'), (21, 20, 'Tenant', '2024-08-01'),
(22, 21, 'Owner', '2024-09-01'), (23, 22, 'Owner', '2024-10-01'), (24, 23, 'Tenant', '2024-11-01'), (25, 24, 'Owner', '2024-12-01'), (26, 25, 'Owner', '2025-01-01'),
(27, 26, 'Tenant', '2025-02-01'), (28, 27, 'Owner', '2025-03-01'), (29, 28, 'Owner', '2025-04-01'), (30, 29, 'Tenant', '2025-05-01'), (31, 30, 'Owner', '2025-06-01'),
(32, 31, 'Owner', '2025-07-01'), (33, 32, 'Tenant', '2025-08-01'), (34, 33, 'Owner', '2025-09-01'), (35, 34, 'Owner', '2025-10-01'), (36, 35, 'Tenant', '2025-11-01');


INSERT INTO visitors (name, id_type, id_number, contact_number) VALUES
('Visitor 01', 'National ID', 'NID-001', '555-7001'), ('Visitor 02', 'Passport', 'PP-002', '555-7002'), ('Visitor 03', 'Driver License', 'DL-003', '555-7003'),
('Visitor 04', 'National ID', 'NID-004', '555-7004'), ('Visitor 05', 'Passport', 'PP-005', '555-7005'), ('Visitor 06', 'Driver License', 'DL-006', '555-7006'),
('Visitor 07', 'National ID', 'NID-007', '555-7007'), ('Visitor 08', 'Passport', 'PP-008', '555-7008'), ('Visitor 09', 'Driver License', 'DL-009', '555-7009'),
('Visitor 10', 'National ID', 'NID-010', '555-7010'), ('Visitor 11', 'Passport', 'PP-011', '555-7011'), ('Visitor 12', 'Driver License', 'DL-012', '555-7012'),
('Visitor 13', 'National ID', 'NID-013', '555-7013'), ('Visitor 14', 'Passport', 'PP-014', '555-7014'), ('Visitor 15', 'Driver License', 'DL-015', '555-7015'),
('Visitor 16', 'National ID', 'NID-016', '555-7016'), ('Visitor 17', 'Passport', 'PP-017', '555-7017'), ('Visitor 18', 'Driver License', 'DL-018', '555-7018'),
('Visitor 19', 'National ID', 'NID-019', '555-7019'), ('Visitor 20', 'Passport', 'PP-020', '555-7020'), ('Visitor 21', 'Driver License', 'DL-021', '555-7021'),
('Visitor 22', 'National ID', 'NID-022', '555-7022'), ('Visitor 23', 'Passport', 'PP-023', '555-7023'), ('Visitor 24', 'Driver License', 'DL-024', '555-7024'),
('Visitor 25', 'National ID', 'NID-025', '555-7025'), ('Visitor 26', 'Passport', 'PP-026', '555-7026'), ('Visitor 27', 'Driver License', 'DL-027', '555-7027'),
('Visitor 28', 'National ID', 'NID-028', '555-7028'), ('Visitor 29', 'Passport', 'PP-029', '555-7029'), ('Visitor 30', 'Driver License', 'DL-030', '555-7030'),
('Visitor 31', 'National ID', 'NID-031', '555-7031'), ('Visitor 32', 'Passport', 'PP-032', '555-7032'), ('Visitor 33', 'Driver License', 'DL-033', '555-7033'),
('Visitor 34', 'National ID', 'NID-034', '555-7034'), ('Visitor 35', 'Passport', 'PP-035', '555-7035'), ('Visitor 36', 'Driver License', 'DL-036', '555-7036'),
('Visitor 37', 'National ID', 'NID-037', '555-7037'), ('Visitor 38', 'Passport', 'PP-038', '555-7038'), ('Visitor 39', 'Driver License', 'DL-039', '555-7039'),
('Visitor 40', 'National ID', 'NID-040', '555-7040');

INSERT INTO access_logs (visitor_id, unit_id, guard_id, entry_time, exit_time, gate_pass_code) VALUES
(1, 1, 37, '2026-02-21 08:00:00', '2026-02-21 10:00:00', 'GPC-001'), (2, 2, 37, '2026-02-21 09:00:00', '2026-02-21 11:00:00', 'GPC-002'),
(3, 3, 38, '2026-02-21 10:00:00', '2026-02-21 12:00:00', 'GPC-003'), (4, 4, 38, '2026-02-21 11:00:00', '2026-02-21 13:00:00', 'GPC-004'),
(5, 5, 37, '2026-02-21 12:00:00', '2026-02-21 14:00:00', 'GPC-005'), (6, 6, 37, '2026-02-21 13:00:00', '2026-02-21 15:00:00', 'GPC-006'),
(7, 7, 38, '2026-02-21 14:00:00', '2026-02-21 16:00:00', 'GPC-007'), (8, 8, 38, '2026-02-21 15:00:00', '2026-02-21 17:00:00', 'GPC-008'),
(9, 9, 37, '2026-02-21 16:00:00', '2026-02-21 18:00:00', 'GPC-009'), (10, 10, 37, '2026-02-21 17:00:00', '2026-02-21 19:00:00', 'GPC-010'),

(11, 11, 37, '2026-02-21 08:30:00', NULL, 'GPC-011'), (12, 12, 38, '2026-02-21 09:30:00', NULL, 'GPC-012'),
(13, 13, 37, '2026-02-21 10:30:00', NULL, 'GPC-013'), (14, 14, 38, '2026-02-21 11:30:00', NULL, 'GPC-014'),
(15, 15, 37, '2026-02-21 12:30:00', NULL, 'GPC-015'), (16, 16, 38, '2026-02-21 13:30:00', NULL, 'GPC-016'),
(17, 17, 37, '2026-02-21 14:30:00', NULL, 'GPC-017'), (18, 18, 38, '2026-02-21 15:30:00', NULL, 'GPC-018'),
(19, 19, 37, '2026-02-21 16:30:00', NULL, 'GPC-019'), (20, 20, 38, '2026-02-21 17:30:00', NULL, 'GPC-020'),
(21, 21, 37, '2026-02-21 08:45:00', '2026-02-21 09:45:00', 'GPC-021'), (22, 22, 38, '2026-02-21 09:45:00', '2026-02-21 10:45:00', 'GPC-022'),
(23, 23, 37, '2026-02-21 10:45:00', '2026-02-21 11:45:00', 'GPC-023'), (24, 24, 38, '2026-02-21 11:45:00', '2026-02-21 12:45:00', 'GPC-024'),
(25, 25, 37, '2026-02-21 12:45:00', '2026-02-21 13:45:00', 'GPC-025'), (26, 26, 38, '2026-02-21 13:45:00', '2026-02-21 14:45:00', 'GPC-026'),
(27, 27, 37, '2026-02-21 14:45:00', '2026-02-21 15:45:00', 'GPC-027'), (28, 28, 38, '2026-02-21 15:45:00', '2026-02-21 16:45:00', 'GPC-028'),
(29, 29, 37, '2026-02-21 16:45:00', '2026-02-21 17:45:00', 'GPC-029'), (30, 30, 38, '2026-02-21 17:45:00', '2026-02-21 18:45:00', 'GPC-030');


INSERT INTO amenities (name, location, capacity, hourly_rate) VALUES
('Swimming Pool', 'Block A Rooftop', 20, 50.00), ('Gymnasium', 'Block B Ground', 15, 30.00),
('Clubhouse', 'Central Park', 50, 200.00), ('Tennis Court', 'East Wing', 4, 100.00), ('Library', 'Block C 1st Floor', 10, 0.00);


INSERT INTO payments (resident_id, amount, payment_date, payment_type, status) VALUES
(1, 5000.00, '2026-01-01', 'Maintenance', 'Paid'), (1, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(2, 5000.00, '2026-01-01', 'Maintenance', 'Paid'), (2, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(3, 5000.00, '2026-01-01', 'Maintenance', 'Paid'), (3, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(4, 5000.00, '2026-01-01', 'Maintenance', 'Paid'), (4, 5000.00, '2026-02-01', 'Maintenance', 'Pending'),
(5, 5000.00, '2026-01-01', 'Maintenance', 'Paid'), (5, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(6, 100.00, '2026-02-10', 'Amenity', 'Paid'), (7, 150.00, '2026-02-11', 'Amenity', 'Paid'),
(8, 200.00, '2026-02-12', 'Amenity', 'Paid'), (9, 250.00, '2026-02-13', 'Amenity', 'Paid'),
(10, 300.00, '2026-02-14', 'Amenity', 'Paid'), (11, 350.00, '2026-02-15', 'Amenity', 'Paid'),
(12, 400.00, '2026-02-16', 'Amenity', 'Paid'), (13, 450.00, '2026-02-17', 'Amenity', 'Paid'),
(14, 500.00, '2026-02-18', 'Amenity', 'Paid'), (15, 550.00, '2026-02-19', 'Amenity', 'Paid'),
(16, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (17, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(18, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (19, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(20, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (21, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(22, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (23, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(24, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (25, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(26, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (27, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(28, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (29, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(30, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (31, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(32, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (33, 5000.00, '2026-02-01', 'Maintenance', 'Paid'),
(34, 5000.00, '2026-02-01', 'Maintenance', 'Paid'), (35, 5000.00, '2026-02-01', 'Maintenance', 'Paid');


INSERT INTO bookings (amenity_id, resident_id, booking_date, start_time, end_time, status) VALUES
(1, 1, '2026-02-22', '09:00:00', '10:00:00', 'Confirmed'), (2, 2, '2026-02-22', '07:00:00', '08:00:00', 'Confirmed'),
(3, 3, '2026-02-23', '18:00:00', '21:00:00', 'Confirmed'), (4, 4, '2026-02-24', '16:00:00', '17:00:00', 'Confirmed'),
(5, 5, '2026-02-25', '10:00:00', '12:00:00', 'Confirmed'), (1, 6, '2026-02-26', '09:00:00', '10:00:00', 'Confirmed'),
(2, 7, '2026-02-27', '07:00:00', '08:00:00', 'Confirmed'), (3, 8, '2026-02-28', '18:00:00', '21:00:00', 'Confirmed'),
(4, 9, '2026-03-01', '16:00:00', '17:00:00', 'Confirmed'), (5, 10, '2026-03-02', '10:00:00', '12:00:00', 'Confirmed');


INSERT INTO complaints (resident_id, title, description, priority, status) VALUES
(1, 'Water Leak', 'Kitchen pipe leaking.', 'High', 'Open'), (2, 'No Power', 'Phase out in Unit 102.', 'High', 'In Progress'),
(3, 'Trash', 'Garbage not collected.', 'Low', 'Resolved'), (4, 'Noise', 'Loud party in Unit 105.', 'Medium', 'Open'),
(5, 'Gym AC', 'AC not cooling.', 'Medium', 'In Progress'), (6, 'Pool', 'Water looks cloudy.', 'High', 'Open'),
(7, 'Elevator', 'Stuck on floor 2.', 'High', 'In Progress'), (8, 'Lights', 'Parking light out.', 'Low', 'Open'),
(9, 'Intercom', 'Buzzer not working.', 'Medium', 'In Progress'), (10, 'Security', 'Unidentified car.', 'Medium', 'Open');
