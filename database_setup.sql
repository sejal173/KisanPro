-- Create Database
CREATE DATABASE IF NOT EXISTS farmer_seed_management;
USE farmer_seed_management;

-- Create Farmers Table
CREATE TABLE IF NOT EXISTS Farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Admins Table
CREATE TABLE IF NOT EXISTS Admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Seeds Table
CREATE TABLE IF NOT EXISTS Seeds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    season VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Orders Table
CREATE TABLE IF NOT EXISTS Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    order_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Pending', 'Approved', 'Delivered') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES Farmers(id) ON DELETE CASCADE
);

-- Create Order_Items Table
CREATE TABLE IF NOT EXISTS Order_Items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    seed_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
    FOREIGN KEY (seed_id) REFERENCES Seeds(id) ON DELETE CASCADE
);

-- Insert Sample Admin (password: admin123)
-- Note: In production, use Werkzeug's generate_password_hash
INSERT INTO Admins (name, email, password) VALUES 
('Admin User', 'admin@kisanpro.com', 'pbkdf2:sha256:600000$XxXxXxXxXxXxXxXx$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');

-- Insert Sample Seeds
INSERT INTO Seeds (name, crop_type, season, price, stock_quantity, description) VALUES
('Premium Wheat Seeds', 'Wheat', 'Rabi', 45.00, 500, 'High-yield wheat seeds suitable for rabi season. Excellent germination rate.'),
('Basmati Rice Seeds', 'Rice', 'Kharif', 55.00, 300, 'Premium quality basmati rice seeds with aromatic grains.'),
('Hybrid Corn Seeds', 'Corn', 'Kharif', 60.00, 400, 'High-yield hybrid corn seeds with disease resistance.'),
('Mustard Seeds', 'Mustard', 'Rabi', 50.00, 250, 'Quality mustard seeds for oil production.'),
('Soybean Seeds', 'Soybean', 'Kharif', 48.00, 350, 'Premium soybean seeds with high protein content.'),
('Cotton Seeds', 'Cotton', 'Kharif', 65.00, 200, 'BT cotton seeds with pest resistance.'),
('Sugarcane Seeds', 'Sugarcane', 'All Season', 70.00, 150, 'High-sugar content sugarcane seeds.'),
('Potato Seeds', 'Potato', 'Rabi', 40.00, 600, 'Certified potato seeds free from diseases.');

-- Note: To create the admin password hash, run this in Python:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('admin123'))
-- Then replace the password hash in the INSERT statement above
