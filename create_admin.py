"""
Script to create an admin account for the Farmer Seed Management System
Run this script to create a new admin user.
"""

from werkzeug.security import generate_password_hash
import mysql.connector
from mysql.connector import Error

def create_admin():
    # Database configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Update with your MySQL password
        'database': 'farmer_seed_management'
    }
    
    # Admin details
    name = input("Enter admin name: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    # Hash the password
    hashed_password = generate_password_hash(password)
    
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Insert admin
        insert_query = "INSERT INTO Admins (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, hashed_password))
        connection.commit()
        
        print(f"Admin '{name}' created successfully!")
        print(f"Email: {email}")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    create_admin()
