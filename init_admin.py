"""
Quick script to initialize admin account
Run: python init_admin.py
"""

from werkzeug.security import generate_password_hash
import pymysql

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sejal@173',
    'database': 'farmer_seed_management',
    'cursorclass': pymysql.cursors.DictCursor
}

def init_admin():
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT * FROM Admins WHERE email = 'admin@kisanpro.com'")
        existing = cursor.fetchone()
        
        if existing:
            print("Admin account already exists!")
            cursor.close()
            conn.close()
            return
        
        # Create default admin
        password = 'admin123'
        hashed_password = generate_password_hash(password)
        
        cursor.execute(
            "INSERT INTO Admins (name, email, password) VALUES (%s, %s, %s)",
            ('Admin User', 'admin@kisanpro.com', hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        print("=" * 50)
        print("Admin account created successfully!")
        print("=" * 50)
        print("Email: admin@kisanpro.com")
        print("Password: admin123")
        print("=" * 50)
        print("Please change the password after first login!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        init_admin()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. MySQL server is running")
        print("2. Database 'farmer_seed_management' exists")
        print("3. MySQL password in this script matches your setup")
