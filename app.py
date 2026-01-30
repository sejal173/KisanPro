from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sejal@173',
    'database': 'farmer_seed_management',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': False
}

def get_db_connection():
    """Get MySQL database connection"""
    return pymysql.connect(**MYSQL_CONFIG)

# Decorator to check if user is logged in as farmer
def farmer_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('farmer_login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check if user is logged in as admin
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login as admin to access this page', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== HOME & STATIC PAGES ====================

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Seeds ORDER BY id DESC LIMIT 6")
        featured_seeds = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        featured_seeds = []
        flash('Error loading featured seeds. Please ensure database is set up.', 'error')
    
    return render_template('home.html', featured_seeds=featured_seeds)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ==================== FARMER AUTHENTICATION ====================

@app.route('/farmer/register', methods=['GET', 'POST'])
def farmer_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        address = request.form['address']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute('SELECT * FROM Farmers WHERE email = %s', (email,))
            account = cursor.fetchone()
            
            if account:
                flash('Email already registered!', 'error')
                cursor.close()
                conn.close()
                return render_template('farmer_register.html')
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Insert farmer
            cursor.execute('INSERT INTO Farmers (name, email, password, contact, address) VALUES (%s, %s, %s, %s, %s)',
                          (name, email, hashed_password, contact, address))
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('farmer_login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('farmer_register.html')
    
    return render_template('farmer_register.html')

@app.route('/farmer/login', methods=['GET', 'POST'])
def farmer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Farmers WHERE email = %s', (email,))
            account = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if account and check_password_hash(account['password'], password):
                session['farmer_id'] = account['id']
                session['farmer_name'] = account['name']
                session['farmer_email'] = account['email']
                flash('Login successful!', 'success')
                return redirect(url_for('seeds_list'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'error')
    
    return render_template('farmer_login.html')

@app.route('/farmer/logout')
def farmer_logout():
    session.pop('farmer_id', None)
    session.pop('farmer_name', None)
    session.pop('farmer_email', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# ==================== ADMIN AUTHENTICATION ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Admins WHERE email = %s', (email,))
            account = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if account and check_password_hash(account['password'], password):
                session['admin_id'] = account['id']
                session['admin_name'] = account['name']
                session['admin_email'] = account['email']
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    session.pop('admin_email', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# ==================== SEEDS ====================

@app.route('/seeds')
def seeds_list():
    crop_type = request.args.get('crop_type', '')
    season = request.args.get('season', '')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM Seeds WHERE 1=1"
        params = []
        
        if crop_type:
            query += " AND crop_type = %s"
            params.append(crop_type)
        
        if season:
            query += " AND season = %s"
            params.append(season)
        
        query += " ORDER BY id DESC"
        
        cursor.execute(query, params)
        seeds = cursor.fetchall()
        
        # Get unique crop types and seasons for filter
        cursor.execute("SELECT DISTINCT crop_type FROM Seeds")
        crop_types = [row['crop_type'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT season FROM Seeds")
        seasons = [row['season'] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
    except Exception as e:
        seeds = []
        crop_types = []
        seasons = []
        flash(f'Error loading seeds: {str(e)}', 'error')
    
    return render_template('seeds_list.html', seeds=seeds, crop_types=crop_types, seasons=seasons, 
                          selected_crop_type=crop_type, selected_season=season)

@app.route('/seeds/<int:seed_id>')
def seed_details(seed_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Seeds WHERE id = %s', (seed_id,))
        seed = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not seed:
            flash('Seed not found!', 'error')
            return redirect(url_for('seeds_list'))
    except Exception as e:
        flash(f'Error loading seed: {str(e)}', 'error')
        return redirect(url_for('seeds_list'))
    
    return render_template('seed_details.html', seed=seed)

# ==================== CART ====================

@app.route('/cart')
@farmer_login_required
def cart():
    if 'cart' not in session:
        session['cart'] = {}
    
    cart_items = []
    total = 0
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for seed_id, quantity in session['cart'].items():
            cursor.execute('SELECT * FROM Seeds WHERE id = %s', (seed_id,))
            seed = cursor.fetchone()
            if seed:
                item_total = float(seed['price']) * int(quantity)
                total += item_total
                cart_items.append({
                    'seed': seed,
                    'quantity': quantity,
                    'total': item_total
                })
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error loading cart: {str(e)}', 'error')
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/add', methods=['POST'])
@farmer_login_required
def add_to_cart():
    seed_id = request.form.get('seed_id')
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if seed_id in session['cart']:
        session['cart'][seed_id] = str(int(session['cart'][seed_id]) + quantity)
    else:
        session['cart'][seed_id] = str(quantity)
    
    session.modified = True
    flash('Item added to cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/update', methods=['POST'])
@farmer_login_required
def update_cart():
    seed_id = request.form.get('seed_id')
    quantity = int(request.form.get('quantity', 0))
    
    if quantity <= 0:
        session['cart'].pop(seed_id, None)
    else:
        session['cart'][seed_id] = str(quantity)
    
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:seed_id>')
@farmer_login_required
def remove_from_cart(seed_id):
    if 'cart' in session and str(seed_id) in session['cart']:
        session['cart'].pop(str(seed_id), None)
        session.modified = True
        flash('Item removed from cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/clear')
@farmer_login_required
def clear_cart():
    session['cart'] = {}
    session.modified = True
    flash('Cart cleared!', 'success')
    return redirect(url_for('cart'))

# ==================== ORDERS ====================

@app.route('/orders', methods=['GET', 'POST'])
@farmer_login_required
def orders():
    if request.method == 'POST':
        # Place order
        if 'cart' not in session or not session['cart']:
            flash('Cart is empty!', 'error')
            return redirect(url_for('cart'))
        
        farmer_id = session['farmer_id']
        total_amount = 0
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Calculate total
            for seed_id, quantity in session['cart'].items():
                cursor.execute('SELECT price FROM Seeds WHERE id = %s', (seed_id,))
                seed = cursor.fetchone()
                if seed:
                    total_amount += float(seed['price']) * int(quantity)
            
            # Create order
            cursor.execute('INSERT INTO Orders (farmer_id, order_date, total_amount, status) VALUES (%s, %s, %s, %s)',
                          (farmer_id, datetime.now(), total_amount, 'Pending'))
            order_id = cursor.lastrowid
            
            # Create order items
            for seed_id, quantity in session['cart'].items():
                cursor.execute('SELECT price FROM Seeds WHERE id = %s', (seed_id,))
                seed = cursor.fetchone()
                if seed:
                    cursor.execute('INSERT INTO Order_Items (order_id, seed_id, quantity, price) VALUES (%s, %s, %s, %s)',
                                  (order_id, seed_id, quantity, seed['price']))
                    # Update stock
                    cursor.execute('UPDATE Seeds SET stock_quantity = stock_quantity - %s WHERE id = %s',
                                  (quantity, seed_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Clear cart
            session['cart'] = {}
            session.modified = True
            
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders'))
        except Exception as e:
            flash(f'Error placing order: {str(e)}', 'error')
            return redirect(url_for('cart'))
    
    # View orders
    farmer_id = session['farmer_id']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Orders WHERE farmer_id = %s ORDER BY order_date DESC', (farmer_id,))
        orders = cursor.fetchall()
        
        # Get order items for each order (use 'order_items' to avoid shadowing dict.items() method)
        for order in orders:
            cursor.execute('''SELECT oi.*, s.name as seed_name 
                             FROM Order_Items oi 
                             JOIN Seeds s ON oi.seed_id = s.id 
                             WHERE oi.order_id = %s''', (order['id'],))
            order['order_items'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
    except Exception as e:
        orders = []
        flash(f'Error loading orders: {str(e)}', 'error')
    
    return render_template('orders.html', orders=orders)

@app.route('/orders/<int:order_id>')
@farmer_login_required
def order_details(order_id):
    farmer_id = session['farmer_id']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Orders WHERE id = %s AND farmer_id = %s', (order_id, farmer_id))
        order = cursor.fetchone()
        
        if not order:
            flash('Order not found!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('orders'))
        
        cursor.execute('''SELECT oi.*, s.name as seed_name, s.crop_type, s.season 
                         FROM Order_Items oi 
                         JOIN Seeds s ON oi.seed_id = s.id 
                         WHERE oi.order_id = %s''', (order_id,))
        order_items = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error loading order: {str(e)}', 'error')
        return redirect(url_for('orders'))
    
    return render_template('order_details.html', order=order, order_items=order_items)

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get statistics
        cursor.execute('SELECT COUNT(*) as total FROM Seeds')
        total_seeds = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM Orders')
        total_orders = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM Farmers')
        total_farmers = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM Orders WHERE status = "Pending"')
        pending_orders = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        stats = {
            'total_seeds': total_seeds,
            'total_orders': total_orders,
            'total_farmers': total_farmers,
            'pending_orders': pending_orders
        }
    except Exception as e:
        stats = {
            'total_seeds': 0,
            'total_orders': 0,
            'total_farmers': 0,
            'pending_orders': 0
        }
        flash(f'Error loading statistics: {str(e)}', 'error')
    
    return render_template('admin_dashboard.html', stats=stats)

# Seed Management
@app.route('/admin/seeds')
@admin_login_required
def admin_seeds():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Seeds ORDER BY id DESC')
        seeds = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        seeds = []
        flash(f'Error loading seeds: {str(e)}', 'error')
    
    return render_template('admin_seeds.html', seeds=seeds)

@app.route('/admin/seeds/add', methods=['GET', 'POST'])
@admin_login_required
def admin_add_seed():
    if request.method == 'POST':
        name = request.form['name']
        crop_type = request.form['crop_type']
        season = request.form['season']
        price = float(request.form['price'])
        stock_quantity = int(request.form['stock_quantity'])
        description = request.form['description']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Seeds (name, crop_type, season, price, stock_quantity, description) 
                             VALUES (%s, %s, %s, %s, %s, %s)''',
                          (name, crop_type, season, price, stock_quantity, description))
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Seed added successfully!', 'success')
            return redirect(url_for('admin_seeds'))
        except Exception as e:
            flash(f'Error adding seed: {str(e)}', 'error')
    
    return render_template('admin_seed_form.html', seed=None)

@app.route('/admin/seeds/edit/<int:seed_id>', methods=['GET', 'POST'])
@admin_login_required
def admin_edit_seed(seed_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if request.method == 'POST':
            name = request.form['name']
            crop_type = request.form['crop_type']
            season = request.form['season']
            price = float(request.form['price'])
            stock_quantity = int(request.form['stock_quantity'])
            description = request.form['description']
            
            cursor.execute('''UPDATE Seeds SET name=%s, crop_type=%s, season=%s, price=%s, 
                             stock_quantity=%s, description=%s WHERE id=%s''',
                          (name, crop_type, season, price, stock_quantity, description, seed_id))
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Seed updated successfully!', 'success')
            return redirect(url_for('admin_seeds'))
        
        cursor.execute('SELECT * FROM Seeds WHERE id = %s', (seed_id,))
        seed = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not seed:
            flash('Seed not found!', 'error')
            return redirect(url_for('admin_seeds'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_seeds'))
    
    return render_template('admin_seed_form.html', seed=seed)

@app.route('/admin/seeds/delete/<int:seed_id>')
@admin_login_required
def admin_delete_seed(seed_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Seeds WHERE id = %s', (seed_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Seed deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting seed: {str(e)}', 'error')
    
    return redirect(url_for('admin_seeds'))

# Order Management
@app.route('/admin/orders')
@admin_login_required
def admin_orders():
    status = request.args.get('status', '')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''SELECT o.*, f.name as farmer_name, f.email as farmer_email 
                             FROM Orders o 
                             JOIN Farmers f ON o.farmer_id = f.id 
                             WHERE o.status = %s 
                             ORDER BY o.order_date DESC''', (status,))
        else:
            cursor.execute('''SELECT o.*, f.name as farmer_name, f.email as farmer_email 
                             FROM Orders o 
                             JOIN Farmers f ON o.farmer_id = f.id 
                             ORDER BY o.order_date DESC''')
        
        orders = cursor.fetchall()
        
        # Get order items for each order (use 'order_items' to avoid shadowing dict.items() method)
        for order in orders:
            cursor.execute('''SELECT oi.*, s.name as seed_name 
                             FROM Order_Items oi 
                             JOIN Seeds s ON oi.seed_id = s.id 
                             WHERE oi.order_id = %s''', (order['id'],))
            order['order_items'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
    except Exception as e:
        orders = []
        flash(f'Error loading orders: {str(e)}', 'error')
    
    return render_template('admin_orders.html', orders=orders, selected_status=status)

@app.route('/admin/orders/<int:order_id>/update-status', methods=['POST'])
@admin_login_required
def admin_update_order_status(order_id):
    new_status = request.form['status']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Orders SET status = %s WHERE id = %s', (new_status, order_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Order status updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating order: {str(e)}', 'error')
    
    return redirect(url_for('admin_orders'))

# Farmer Management
@app.route('/admin/farmers')
@admin_login_required
def admin_farmers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, contact, address FROM Farmers ORDER BY id DESC')
        farmers = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        farmers = []
        flash(f'Error loading farmers: {str(e)}', 'error')
    
    return render_template('admin_farmers.html', farmers=farmers)

@app.route('/admin/farmers/delete/<int:farmer_id>')
@admin_login_required
def admin_delete_farmer(farmer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Farmers WHERE id = %s', (farmer_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Farmer deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting farmer: {str(e)}', 'error')
    
    return redirect(url_for('admin_farmers'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
