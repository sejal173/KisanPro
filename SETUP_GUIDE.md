# Setup Guide - Farmer Seed Management System

## Step 1: Install MySQL

If MySQL is not installed, download and install it from:
- Windows: https://dev.mysql.com/downloads/installer/
- Or use XAMPP/WAMP which includes MySQL

## Step 2: Configure MySQL Password

1. Open MySQL command line or MySQL Workbench
2. If you haven't set a password, you can set one:
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
   ```

## Step 3: Update Configuration

Edit these files and update the MySQL password:

1. **app.py** (line 15):
   ```python
   'password': 'your_mysql_password',  # Update this
   ```

2. **setup_database.py** (line 10):
   ```python
   'password': 'your_mysql_password',  # Update this
   ```

3. **init_admin.py** (line 7):
   ```python
   'password': 'your_mysql_password',  # Update this
   ```

## Step 4: Set Up Database

Run the database setup script:
```bash
python setup_database.py
```

This will:
- Create the database
- Create all tables
- Create default admin account (admin@kisanpro.com / admin123)
- Insert sample seed data

## Step 5: Run the Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

## Default Login Credentials

**Admin:**
- Email: admin@kisanpro.com
- Password: admin123

**Farmer:**
- Register a new account at /farmer/register

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Check MySQL password in configuration files
- Verify MySQL is installed and accessible

### Port Already in Use
- Change port in app.py: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Database Not Found
- Run `python setup_database.py` to create the database

### Module Not Found
- Run `pip install -r requirements.txt`
