"""
Database setup script for Farmer Seed Management System
This script creates the database and tables if they don't exist.
"""

import pymysql
from werkzeug.security import generate_password_hash

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sejal@173',
    'cursorclass': pymysql.cursors.DictCursor
}

def setup_database():
    try:
        # Connect to MySQL server (without database)
        conn = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            cursorclass=MYSQL_CONFIG['cursorclass']
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS farmer_seed_management")
        cursor.execute("USE farmer_seed_management")
        
        print("Database created/selected successfully!")
        
        # Create Farmers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Farmers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                contact VARCHAR(20) NOT NULL,
                address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Farmers table created!")
        
        # Create Admins Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Admins table created!")
        
        # Create Seeds Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Seeds (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                crop_type VARCHAR(50) NOT NULL,
                season VARCHAR(50) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock_quantity INT NOT NULL DEFAULT 0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Seeds table created!")
        
        # Create Orders Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                farmer_id INT NOT NULL,
                order_date DATETIME NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                status ENUM('Pending', 'Approved', 'Delivered') DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farmer_id) REFERENCES Farmers(id) ON DELETE CASCADE
            )
        """)
        print("Orders table created!")
        
        # Create Order_Items Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Order_Items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                seed_id INT NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
                FOREIGN KEY (seed_id) REFERENCES Seeds(id) ON DELETE CASCADE
            )
        """)
        print("Order_Items table created!")
        
        # Check if admin exists
        cursor.execute("SELECT * FROM Admins WHERE email = 'admin@kisanpro.com'")
        admin_exists = cursor.fetchone()
        
        if not admin_exists:
            # Create default admin
            password = 'admin123'
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO Admins (name, email, password) VALUES (%s, %s, %s)",
                ('Admin User', 'admin@kisanpro.com', hashed_password)
            )
            print("Default admin account created!")
            print("Email: admin@kisanpro.com")
            print("Password: admin123")
        
        # Check if seeds exist, if not insert sample data
        cursor.execute("SELECT COUNT(*) as count FROM Seeds")
        seed_count = cursor.fetchone()['count']
        
        if seed_count == 0:
            sample_seeds = [
                ('Premium Wheat Seeds', 'Wheat', 'Rabi', 45.00, 500, 'High-yield wheat seeds suitable for rabi season. Excellent germination rate.'),
                ('Basmati Rice Seeds', 'Rice', 'Kharif', 55.00, 300, 'Premium quality basmati rice seeds with aromatic grains.'),
                ('Hybrid Corn Seeds', 'Corn', 'Kharif', 60.00, 400, 'High-yield hybrid corn seeds with disease resistance.'),
                ('Mustard Seeds', 'Mustard', 'Rabi', 50.00, 250, 'Quality mustard seeds for oil production.'),
                ('Soybean Seeds', 'Soybean', 'Kharif', 48.00, 350, 'Premium soybean seeds with high protein content.'),
                ('Cotton Seeds', 'Cotton', 'Kharif', 65.00, 200, 'BT cotton seeds with pest resistance.'),
                ('Sugarcane Seeds', 'Sugarcane', 'All Season', 70.00, 150, 'High-sugar content sugarcane seeds.'),
                ('Potato Seeds', 'Potato', 'Rabi', 40.00, 600, 'Certified potato seeds free from diseases.')
            ]
            
            cursor.executemany(
                """INSERT INTO Seeds (name, crop_type, season, price, stock_quantity, description) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                sample_seeds
            )
            print(f"Inserted {len(sample_seeds)} sample seeds!")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("Database setup completed successfully!")
        print("="*50)
        
    except pymysql.Error as e:
        print(f"MySQL Error: {e}")
        print("\nPlease ensure:")
        print("1. MySQL server is running")
        print("2. MySQL password in this script is correct")
        print("3. You have permission to create databases")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_database()
