

DROP DATABASE IF EXISTS gated_community_db;
CREATE DATABASE gated_community_db;
USE gated_community_db;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL
);


CREATE TABLE units (
    id INT AUTO_INCREMENT PRIMARY KEY,
    unit_number VARCHAR(10) NOT NULL,
    block VARCHAR(10),
    unit_type ENUM('1BHK', '2BHK', '3BHK', 'Villa') DEFAULT '2BHK',
    square_feet INT,
    CHECK (square_feet > 0)
);


CREATE TABLE residents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    unit_id INT NOT NULL,
    residency_status ENUM('Owner', 'Tenant') DEFAULT 'Owner',
    move_in_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE
);


CREATE TABLE visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    id_type ENUM('Passport', 'National ID', 'Driver License') NOT NULL,
    id_number VARCHAR(50) NOT NULL UNIQUE,
    contact_number VARCHAR(20)
);


CREATE TABLE access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visitor_id INT NOT NULL,
    unit_id INT NOT NULL,
    guard_id INT NOT NULL,
    entry_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    exit_time DATETIME NULL,
    gate_pass_code VARCHAR(20),
    FOREIGN KEY (visitor_id) REFERENCES visitors(id),
    FOREIGN KEY (unit_id) REFERENCES units(id),
    FOREIGN KEY (guard_id) REFERENCES users(id)
);


CREATE TABLE amenities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    capacity INT NOT NULL,
    hourly_rate DECIMAL(10, 2) DEFAULT 0.00,
    CHECK (capacity > 0)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amenity_id INT NOT NULL,
    resident_id INT NOT NULL,
    booking_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (amenity_id) REFERENCES amenities(id),
    FOREIGN KEY (resident_id) REFERENCES residents(id)
);


CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resident_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_type ENUM('Maintenance', 'Amenity', 'Fine') NOT NULL,
    status ENUM('Paid', 'Pending', 'Overdue') DEFAULT 'Pending',
    CHECK (amount > 0),
    FOREIGN KEY (resident_id) REFERENCES residents(id)
);


CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resident_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    status ENUM('Open', 'In Progress', 'Resolved') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (resident_id) REFERENCES residents(id)
);


CREATE TABLE staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    department VARCHAR(50),
    employee_id VARCHAR(20) UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_logs_entry ON access_logs(entry_time);
CREATE INDEX idx_payments_status ON payments(status);


CREATE OR REPLACE VIEW view_daily_visitors AS
SELECT v.name AS visitor_name, u.unit_number, al.entry_time, al.exit_time
FROM access_logs al
JOIN visitors v ON al.visitor_id = v.id
JOIN units u ON al.unit_id = u.id
WHERE DATE(al.entry_time) = CURDATE();


CREATE OR REPLACE VIEW view_resident_dues AS
SELECT r.id AS resident_id, u.username, SUM(p.amount) AS total_pending
FROM residents r
JOIN users u ON r.user_id = u.id
JOIN payments p ON r.id = p.resident_id
WHERE p.status = 'Pending' OR p.status = 'Overdue'
GROUP BY r.id;


CREATE OR REPLACE VIEW view_active_bookings AS
SELECT a.name AS amenity_name, b.booking_date, b.start_time, b.end_time, res.id AS resident_id
FROM bookings b
JOIN amenities a ON b.amenity_id = a.id
JOIN residents res ON b.resident_id = res.id
WHERE b.status = 'Confirmed' AND b.booking_date >= CURDATE();


DELIMITER //


CREATE TRIGGER trg_complaint_resolution
BEFORE UPDATE ON complaints
FOR EACH ROW
BEGIN
    IF NEW.status = 'Resolved' AND OLD.status <> 'Resolved' THEN
        SET NEW.resolved_at = CURRENT_TIMESTAMP;
    END IF;
END //


CREATE TRIGGER trg_check_overdue_payments
BEFORE INSERT ON bookings
FOR EACH ROW
BEGIN
    DECLARE overdue_count INT;
    SELECT COUNT(*) INTO overdue_count
    FROM payments
    WHERE resident_id = NEW.resident_id AND status = 'Overdue';
    
    IF overdue_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Booking denied: Resident has overdue payments.';
    END IF;
END //

DELIMITER ;
