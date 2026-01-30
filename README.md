# Farmer Seed Management Website (KisanPro)

A complete web application for managing farmer seed orders with separate interfaces for farmers and administrators.

## Features

### Farmer Features
- User registration and login
- Browse and search seeds by crop type and season
- View detailed seed information
- Add seeds to shopping cart
- Place orders
- View order history and track order status

### Admin Features
- Admin login
- Manage seeds (Add, Edit, Delete)
- View and manage all orders
- Update order status (Pending, Approved, Delivered)
- View and manage farmer accounts
- Dashboard with statistics

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Session-based with password hashing

## Installation

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd KisanPro
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up MySQL Database

1. Open MySQL command line or MySQL Workbench
2. Run the `database_setup.sql` file to create the database and tables:

```bash
mysql -u root -p < database_setup.sql
```

Or manually execute the SQL commands in `database_setup.sql`

### Step 4: Configure Database Connection

Edit `app.py` and update the MySQL configuration:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'  # Update this
app.config['MYSQL_DB'] = 'farmer_seed_management'
```

### Step 5: Create Admin Account

To create an admin account, run this Python script:

```python
from werkzeug.security import generate_password_hash
password_hash = generate_password_hash('your_admin_password')
print(password_hash)
```

Then insert the admin into the database:

```sql
INSERT INTO Admins (name, email, password) VALUES 
('Admin Name', 'admin@kisanpro.com', 'paste_the_hash_here');
```

Or use the sample admin from `database_setup.sql` (you'll need to update the password hash).

### Step 6: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
KisanPro/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database_setup.sql     # Database schema and sample data
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── farmer_login.html
│   ├── farmer_register.html
│   ├── admin_login.html
│   ├── seeds_list.html
│   ├── seed_details.html
│   ├── cart.html
│   ├── orders.html
│   ├── order_details.html
│   ├── admin_dashboard.html
│   ├── admin_seeds.html
│   ├── admin_seed_form.html
│   ├── admin_orders.html
│   ├── admin_farmers.html
│   ├── about.html
│   └── contact.html
└── static/
    ├── css/
    │   └── style.css      # Main stylesheet
    └── js/
        └── main.js        # JavaScript functions
```

## Usage

### For Farmers

1. Register a new account at `/farmer/register`
2. Login at `/farmer/login`
3. Browse seeds at `/seeds`
4. Add seeds to cart and place orders
5. View order history at `/orders`

### For Admins

1. Login at `/admin/login`
2. Access dashboard at `/admin/dashboard`
3. Manage seeds at `/admin/seeds`
4. Manage orders at `/admin/orders`
5. Manage farmers at `/admin/farmers`

## Database Schema

- **Farmers**: Stores farmer account information
- **Admins**: Stores admin account information
- **Seeds**: Stores seed product information
- **Orders**: Stores order information
- **Order_Items**: Stores individual items in each order

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control (Farmer/Admin)
- SQL injection prevention using parameterized queries

## Future Enhancements

- Email notifications for order status updates
- Payment gateway integration
- Advanced search and filtering
- Product reviews and ratings
- Image uploads for seeds
- Order cancellation by farmers
- Stock alerts for low inventory

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please contact: support@kisanpro.com

## Recent Updates
- Improved UI components
- Project structure finalized
- Database connection verified
