-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS inventory_db;

USE inventory_db;

-- Table for Products
CREATE TABLE product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- Table for Locations
CREATE TABLE location (
    location_id VARCHAR(50) PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL
);

-- Table for Product Movements
CREATE TABLE productmovement (
    movement_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    from_location_id VARCHAR(50),
    to_location_id VARCHAR(50),
    product_id VARCHAR(50) NOT NULL,
    qty INT NOT NULL,
    FOREIGN KEY (from_location_id) REFERENCES location(location_id),
    FOREIGN KEY (to_location_id) REFERENCES location(location_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
