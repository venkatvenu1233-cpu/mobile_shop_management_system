from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime
import os
import hashlib
import secrets
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Custom Jinja2 filter to parse JSON
@app.template_filter('from_json')
def from_json(value):
    if value is None:
        return []
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return []

# Password hashing functions
def hash_password(password):
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return salt + password_hash

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    salt = hashed_password[:32]  # First 32 characters are the salt
    stored_hash = hashed_password[32:]  # Rest is the hash
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash == stored_hash

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT DEFAULT 'mobile',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if category column exists, if not add it
    cursor.execute("PRAGMA table_info(products)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'category' not in columns:
        cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "mobile"')
        conn.commit()
    
    # Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Users table with enhanced security
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_password = hash_password('admin123')
        cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)", 
                      ('admin', admin_password, 'admin@mobileshop.com', 1))
    
    # Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT,
            service_type TEXT NOT NULL,
            device_details TEXT,
            issue_description TEXT,
            status TEXT DEFAULT 'Pending',
            cost REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    
    # Orders table for complete order information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE,
            customer_name TEXT NOT NULL,
            items TEXT,  -- JSON string of items
            total REAL NOT NULL,
            address TEXT,
            payment_method TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    conn.commit()
    conn.close()

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login route
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', 
                          (username,)).fetchone()
        conn.close()
        
        if user and verify_password(password, user['password']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('user/login.html')

# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND is_admin = 1', 
                          (username,)).fetchone()
        conn.close()
        
        if user and verify_password(password, user['password']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    
    return render_template('admin/admin_login.html')

# Admin dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Admin access required!', 'error')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    
    # Get statistics
    total_products = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    low_stock_items = conn.execute('SELECT COUNT(*) FROM products WHERE quantity <= 10').fetchone()[0]
    
    # Get today's sales
    today_sales = conn.execute('SELECT COALESCE(SUM(total), 0) FROM sales WHERE DATE(date) = DATE("now", "localtime")').fetchone()[0]
    total_revenue = conn.execute('SELECT COALESCE(SUM(total), 0) FROM sales').fetchone()[0]
    
    # Get services statistics
    total_services = conn.execute('SELECT COUNT(*) FROM services').fetchone()[0]
    pending_services = conn.execute('SELECT COUNT(*) FROM services WHERE status = "Pending"').fetchone()[0]
    completed_services = conn.execute('SELECT COUNT(*) FROM services WHERE status = "Completed"').fetchone()[0]
    service_revenue = conn.execute('SELECT COALESCE(SUM(cost), 0) FROM services WHERE status = "Completed"').fetchone()[0]
    
    # Get products and orders with product details
    mobiles = conn.execute("SELECT * FROM products WHERE category = 'mobile' OR category IS NULL ORDER BY id DESC").fetchall()
    accessories = conn.execute("SELECT * FROM products WHERE category = 'accessory' ORDER BY id DESC").fetchall()
    products = conn.execute('SELECT * FROM products ORDER BY id DESC LIMIT 10').fetchall()
    orders = conn.execute('SELECT * FROM orders ORDER BY date DESC LIMIT 10').fetchall()
    print(f"DEBUG - Found {len(orders)} orders")  # Debug logging
    services = conn.execute('SELECT * FROM services ORDER BY created_at DESC LIMIT 10').fetchall()
    
    # Get low stock items
    low_stock_products = conn.execute('SELECT * FROM products WHERE quantity <= 10 ORDER BY quantity ASC LIMIT 5').fetchall()
    
    conn.close()
    
    return render_template('admin/admin_dashboard.html', 
                     total_products=total_products,
                     low_stock_items=low_stock_items,
                     today_sales=today_sales,
                     total_revenue=total_revenue,
                     total_services=total_services,
                     pending_services=pending_services,
                     completed_services=completed_services,
                     service_revenue=service_revenue,
                     products=products,
                     mobiles=mobiles,
                     accessories=accessories,
                     orders=orders,
                     services=services,
                     low_stock_products=low_stock_products)

# Admin add product route
@app.route('/admin/add_product', methods=['POST'])
def admin_add_product():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    brand = request.form['brand']
    model = request.form['model']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    category = request.form.get('category', 'mobile')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO products (brand, model, price, quantity, category) VALUES (?, ?, ?, ?, ?)',
                 (brand, model, price, quantity, category))
    conn.commit()
    conn.close()
    
    flash('Product added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin set all mobiles to 10 quantity route
@app.route('/admin/init_mobile_stock')
def init_mobile_stock():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if category column exists
    cursor.execute("PRAGMA table_info(products)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add category column if it doesn't exist
    if 'category' not in columns:
        cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "mobile"')
        conn.commit()
    
    # Define all mobile products from mobiles.html
    mobiles_data = [
        # Apple
        ('Apple', 'iPhone 15 Pro Max', 139999, 10),
        ('Apple', 'iPhone 15', 79999, 10),
        ('Apple', 'iPhone 15 Plus', 89999, 10),
        ('Apple', 'iPhone 15 Pro', 119999, 10),
        ('Apple', 'iPhone 14 Pro Max', 129999, 10),
        ('Apple', 'iPhone 14 Pro', 109999, 10),
        ('Apple', 'iPhone 14', 69999, 10),
        ('Apple', 'iPhone 14 Plus', 79999, 10),
        ('Apple', 'iPhone 13 Pro Max', 119999, 10),
        ('Apple', 'iPhone 13 Pro', 99999, 10),
        ('Apple', 'iPhone SE (2022)', 39999, 10),
        # Samsung
        ('Samsung', 'Galaxy S24 Ultra', 124999, 10),
        ('Samsung', 'Galaxy S24', 79999, 10),
        ('Samsung', 'Galaxy S24 Plus', 99999, 10),
        ('Samsung', 'Galaxy S23 Ultra', 109999, 10),
        ('Samsung', 'Galaxy S23', 69999, 10),
        ('Samsung', 'Galaxy S23 Plus', 89999, 10),
        ('Samsung', 'Galaxy Z Fold 5', 154999, 10),
        ('Samsung', 'Galaxy Z Flip 5', 99999, 10),
        ('Samsung', 'Galaxy S22 Ultra', 94999, 10),
        ('Samsung', 'Galaxy S22', 54999, 10),
        ('Samsung', 'Galaxy A54', 38999, 10),
        ('Samsung', 'Galaxy A34', 30999, 10),
        # OnePlus
        ('OnePlus', 'OnePlus 12 Pro', 64999, 10),
        ('OnePlus', 'OnePlus 12', 54999, 10),
        ('OnePlus', 'OnePlus 11', 44999, 10),
        ('OnePlus', 'OnePlus 11R', 39999, 10),
        ('OnePlus', 'OnePlus 10 Pro', 49999, 10),
        ('OnePlus', 'OnePlus 10T', 42999, 10),
        ('OnePlus', 'Nord CE 3', 26999, 10),
        ('OnePlus', 'Nord 3', 33999, 10),
        ('OnePlus', 'Nord 2T', 28999, 10),
        ('OnePlus', 'Ace 2', 29999, 10),
        # Xiaomi
        ('Xiaomi', 'Xiaomi 14 Pro', 54999, 10),
        ('Xiaomi', 'Xiaomi 14', 49999, 10),
        ('Xiaomi', 'Xiaomi 13 Pro', 59999, 10),
        ('Xiaomi', 'Redmi Note 13 Pro Plus', 29999, 10),
        ('Xiaomi', 'Redmi Note 13 Pro', 24999, 10),
        ('Xiaomi', 'Redmi Note 12 Pro Plus', 26999, 10),
        ('Xiaomi', 'Poco X5 Pro', 19999, 10),
        ('Xiaomi', 'Poco X4 Pro', 22999, 10),
        ('Xiaomi', 'Redmi 12', 14999, 10),
        ('Xiaomi', 'Poco F5', 29999, 10),
        ('Xiaomi', 'Poco X6 Pro', 26999, 10),
        # Google
        ('Google', 'Pixel 8 Pro', 109999, 10),
        ('Google', 'Pixel 8', 79999, 10),
        ('Google', 'Pixel 7a', 43999, 10),
        # Vivo
        ('Vivo', 'V30 Pro', 44999, 10),
        ('Vivo', 'X100', 79999, 10),
        ('Vivo', 'V29', 34999, 10),
        ('Vivo', 'T2 Pro', 23999, 10),
        # Oppo
        ('Oppo', 'Find X7 Ultra', 74999, 10),
        ('Oppo', 'Reno 11 Pro', 39999, 10),
        ('Oppo', 'Reno 10 Pro', 34999, 10),
        ('Oppo', 'F25 Pro', 25999, 10),
        # Realme
        ('Realme', 'GT 5 Pro', 44999, 10),
        ('Realme', '12 Pro Plus', 32999, 10),
        ('Realme', 'Narzo 60 Pro', 25999, 10),
        ('Realme', '11 Pro Plus', 29999, 10),
        # Nothing
        ('Nothing', 'Phone 2', 44999, 10),
        ('Nothing', 'Phone 2a', 27999, 10),
        # Motorola
        ('Motorola', 'Edge 40 Pro', 54999, 10),
        ('Motorola', 'Edge 40 Neo', 25999, 10),
        ('Motorola', 'G84', 19999, 10),
        # iQOO
        ('iQOO', '12 Pro', 59999, 10),
        ('iQOO', '12', 52999, 10),
        ('iQOO', 'Neo 9 Pro', 36999, 10),
        # Infinix
        ('Infinix', 'Zero 30', 24999, 10),
        ('Infinix', 'GT 10 Pro', 21999, 10),
        # Tecno
        ('Tecno', 'Phantom V2 Fold', 99999, 10),
        ('Tecno', 'Phantom V2 Flip', 54999, 10),
    ]
    
    # Clear existing mobile products to avoid duplicates
    cursor.execute('DELETE FROM products WHERE category = "mobile" OR category IS NULL')
    
    # Insert all mobile products
    inserted_count = 0
    for brand, model, price, quantity in mobiles_data:
        try:
            cursor.execute(
                'INSERT INTO products (brand, model, price, quantity, category) VALUES (?, ?, ?, ?, ?)',
                (brand, model, price, quantity, 'mobile')
            )
            inserted_count += 1
        except Exception as e:
            print(f'Error inserting {brand} {model}: {e}')
    
    conn.commit()
    conn.close()
    
    flash(f'Mobile stock initialized successfully! ({inserted_count} products added with 10 quantity each)', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin delete product route
@app.route('/admin/delete_product/<int:product_id>')
def admin_delete_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin add sale route
@app.route('/admin/add_sale', methods=['POST'])
def admin_add_sale():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    customer_name = request.form['customer_name']
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    
    conn = get_db_connection()
    
    # Get product details
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if product and product['quantity'] >= quantity:
        # Calculate total
        total = product['price'] * quantity
        
        # Add sale
        conn.execute('INSERT INTO sales (customer_name, product_id, quantity, total, date) VALUES (?, ?, ?, ?, ?)',
                     (customer_name, product_id, quantity, total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # Update product quantity
        new_quantity = product['quantity'] - quantity
        conn.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, product_id))
        
        conn.commit()
        flash('Sale added successfully!', 'success')
    else:
        flash('Insufficient stock!', 'error')
    
    conn.close()
    return redirect(url_for('admin_dashboard'))

# Admin delete sale route
@app.route('/admin/delete_sale/<int:sale_id>')
def admin_delete_sale(sale_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    conn.execute('DELETE FROM sales WHERE id = ?', (sale_id,))
    conn.commit()
    conn.close()
    
    flash('Sale deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin add service route
@app.route('/admin/add_service', methods=['POST'])
def admin_add_service():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    customer_name = request.form.get('customer_name')
    phone = request.form.get('phone')
    service_type = request.form.get('service_type')
    device_details = request.form.get('device_details')
    issue_description = request.form.get('issue_description')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO services (customer_name, phone, service_type, device_details, issue_description, status)
        VALUES (?, ?, ?, ?, ?, 'Pending')
    ''', (customer_name, phone, service_type, device_details, issue_description))
    conn.commit()
    conn.close()
    
    flash('Service registered successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin complete service route
@app.route('/admin/complete_service/<int:service_id>', methods=['POST'])
def admin_complete_service(service_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    cost = request.form.get('cost', 0)
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE services 
        SET status = 'Completed', cost = ?, completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (float(cost), service_id))
    conn.commit()
    conn.close()
    
    flash('Service marked as completed!', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin delete service route
@app.route('/admin/delete_service/<int:service_id>')
def admin_delete_service(service_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    conn.execute('DELETE FROM services WHERE id = ?', (service_id,))
    conn.commit()
    conn.close()
    
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin get service details API
@app.route('/admin/get_service/<int:service_id>')
def admin_get_service(service_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
    conn.close()
    
    if service:
        # Parse device_details and issue_description to extract individual fields
        device_details = service['device_details'] or ''
        issue_desc = service['issue_description'] or ''
        
        # Extract fields from stored text
        device_brand = ''
        device_model = ''
        device_color = ''
        if device_details:
            parts = device_details.split('(')
            if len(parts) > 1:
                device_color = parts[1].rstrip(')')
            brand_model = parts[0].strip().split(' ', 1)
            if len(brand_model) > 0:
                device_brand = brand_model[0]
            if len(brand_model) > 1:
                device_model = brand_model[1]
        
        # Extract condition and other fields from issue_description
        phone_condition = ''
        physical_damage = ''
        phone_turning_on = ''
        has_back_cover = ''
        has_sim_card = ''
        has_memory_card = ''
        problem_description = issue_desc
        
        if 'Condition:' in issue_desc:
            lines = issue_desc.split('\n')
            for line in lines:
                if line.startswith('Condition:'):
                    phone_condition = line.replace('Condition:', '').strip()
                elif line.startswith('Physical damage:'):
                    physical_damage = line.replace('Physical damage:', '').strip()
                elif line.startswith('Phone turning on:'):
                    phone_turning_on = line.replace('Phone turning on:', '').strip()
                elif line.startswith('Back cover:'):
                    has_back_cover = line.replace('Back cover:', '').strip()
                elif line.startswith('SIM card:'):
                    has_sim_card = line.replace('SIM card:', '').strip()
                elif line.startswith('Memory card:'):
                    has_memory_card = line.replace('Memory card:', '').strip()
                elif line.startswith('Issue:'):
                    problem_description = line.replace('Issue:', '').strip()
        
        return jsonify({
            'id': service['id'],
            'customer_name': service['customer_name'],
            'phone': service['phone'],
            'service_type': service['service_type'],
            'device_details': device_details,
            'device_brand': device_brand,
            'device_model': device_model,
            'device_color': device_color,
            'phone_condition': phone_condition,
            'physical_damage': physical_damage,
            'phone_turning_on': phone_turning_on,
            'has_back_cover': has_back_cover,
            'has_sim_card': has_sim_card,
            'has_memory_card': has_memory_card,
            'issue_description': problem_description,
            'status': service['status'],
            'cost': service['cost'],
            'created_at': service['created_at']
        })
    else:
        return jsonify({'error': 'Service not found'}), 404

# Admin get product details API
@app.route('/admin/get_product/<int:product_id>')
def admin_get_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    if product:
        return jsonify({
            'id': product['id'],
            'brand': product['brand'],
            'model': product['model'],
            'price': product['price'],
            'quantity': product['quantity'],
            'category': product['category'] or 'mobile'
        })
    else:
        return jsonify({'error': 'Product not found'}), 404

# Admin edit product route
@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
def admin_edit_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    brand = request.form.get('brand')
    model = request.form.get('model')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    category = request.form.get('category', 'mobile')
    
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE products 
            SET brand = ?, model = ?, price = ?, quantity = ?, category = ?
            WHERE id = ?
        ''', (brand, model, float(price), int(quantity), category, product_id))
        conn.commit()
        conn.close()
        flash('Product updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating product: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

# Admin get order details API
@app.route('/admin/get_order/<int:order_id>')
def admin_get_order(order_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    
    if order:
        return jsonify({
            'id': order['id'],
            'order_id': order['order_id'],
            'customer_name': order['customer_name'],
            'items': order['items'],
            'total': order['total'],
            'address': order['address'],
            'payment_method': order['payment_method'],
            'date': order['date'][:10] if order['date'] else 'N/A',
            'status': order['status'] or 'pending'
        })
    else:
        return jsonify({'error': 'Order not found'}), 404

# Admin edit order route
@app.route('/admin/edit_order/<int:order_id>', methods=['POST'])
def admin_edit_order(order_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    customer_name = request.form.get('customer_name')
    total = request.form.get('total')
    status = request.form.get('status')
    address = request.form.get('address')
    
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE orders 
            SET customer_name = ?, total = ?, status = ?, address = ?
            WHERE id = ?
        ''', (customer_name, float(total), status, address, order_id))
        conn.commit()
        conn.close()
        flash('Order updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating order: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

# Admin get sale details API
@app.route('/admin/get_sale/<int:sale_id>')
def admin_get_sale(sale_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = get_db_connection()
    sale = conn.execute('''
        SELECT s.*, p.brand, p.model, p.price as product_price
        FROM sales s
        LEFT JOIN products p ON s.product_id = p.id
        WHERE s.id = ?
    ''', (sale_id,)).fetchone()
    conn.close()
    
    if sale:
        return jsonify({
            'id': sale['id'],
            'customer_name': sale['customer_name'],
            'product_id': sale['product_id'],
            'brand': sale['brand'],
            'model': sale['model'],
            'product_price': sale['product_price'],
            'quantity': sale['quantity'],
            'total': sale['total'],
            'date': sale['date'][:10] if sale['date'] else 'N/A'
        })
    else:
        return jsonify({'error': 'Sale not found'}), 404

# API endpoint to place order from checkout
@app.route('/api/place_order', methods=['POST'])
def api_place_order():
    print(f"DEBUG - Session data: {session}")  # Debug logging
    
    data = request.get_json()
    print(f"DEBUG - Order received: {data}")  # Debug logging
    
    try:
        conn = get_db_connection()
        
        # Validate required data
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        items = data.get('items', [])
        if not items:
            return jsonify({'error': 'No items in order'}), 400
        
        print(f"DEBUG - Processing {len(items)} items")
        
        # Get user details if logged in, otherwise use guest
        customer_name = data.get('customer_name', 'Guest')
        if 'user_id' in session:
            user = conn.execute('SELECT username, email FROM users WHERE id = ?', 
                              (session['user_id'],)).fetchone()
            if user:
                customer_name = user['username']
                print(f"DEBUG - Logged in user: {customer_name}")
        else:
            print("DEBUG - Guest user placing order")
        
        # Process each item in the order
        total_amount = 0
        order_items = []
        
        for i, item in enumerate(items):
            print(f"DEBUG - Processing item {i}: {item}")
            # For each item, create a sale record
            product_id = item.get('product_id', 1)
            quantity = item.get('quantity', 1) or item.get('qty', 1)
            price = item.get('price', 0)
            item_total = price * quantity
            total_amount += item_total
            
            print(f"DEBUG - Inserting sale: customer={customer_name}, product_id={product_id}, qty={quantity}, total={item_total}")
            
            # Add to sales table with complete order information
            conn.execute('''
                INSERT INTO sales (customer_name, product_id, quantity, total, date) 
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_name, product_id, quantity, item_total, 
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            order_items.append({
                'name': item.get('name', 'Product'),
                'brand': item.get('brand', 'Unknown'),
                'quantity': quantity,
                'price': price
            })
        
        # Also store complete order in orders table for detailed view
        order_id = data.get('order_id', '')
        address = data.get('address', '')
        payment_method = data.get('payment_method', '')
        
        print(f"DEBUG - Inserting order: id={order_id}, customer={customer_name}, total={total_amount}")
        print(f"DEBUG - Items JSON: {json.dumps(items)}")
        
        conn.execute('''
            INSERT INTO orders (order_id, customer_name, items, total, address, payment_method, date, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_id,
            customer_name,
            json.dumps(items),  # Store items as JSON
            total_amount,
            address,
            payment_method,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'pending'
        ))
        
        print(f"DEBUG - Order saved to orders table: {data.get('order_id')}")
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Order placed successfully',
            'order_id': data.get('order_id'),
            'total': total_amount
        }), 200
        
    except Exception as e:
        import traceback
        print(f"DEBUG - Error: {e}")
        print(f"DEBUG - Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('user/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('user/register.html')
        
        conn = get_db_connection()
        
        # Check if username already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', 
                                   (username,)).fetchone()
        if existing_user:
            flash('Username already exists!', 'error')
            conn.close()
            return render_template('user/register.html')
        
        # Check if email already exists
        existing_email = conn.execute('SELECT * FROM users WHERE email = ?', 
                                    (email,)).fetchone()
        if existing_email:
            flash('Email already registered!', 'error')
            conn.close()
            return render_template('user/register.html')
        
        # Create new user
        hashed_password = hash_password(password)
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('user/register.html')

# Forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user:
            # In a real application, you would send an email with a reset link
            # For this demo, we'll show a success message and reset to a default password
            temp_password = 'temp123'
            hashed_temp = hash_password(temp_password)
            
            conn = get_db_connection()
            conn.execute('UPDATE users SET password = ? WHERE email = ?', 
                        (hashed_temp, email))
            conn.commit()
            conn.close()
            
            flash(f'Password reset successful! Your temporary password is: {temp_password}', 'success')
            flash('Please login and change your password immediately.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email not found in our system!', 'error')
    
    return render_template('forgot_password.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get statistics
    total_products = conn.execute('SELECT COUNT(*) as count FROM products').fetchone()['count']
    total_sales = conn.execute('SELECT COUNT(*) as count FROM sales').fetchone()['count']
    total_customers = conn.execute('SELECT COUNT(*) as count FROM customers').fetchone()['count']
    total_revenue = conn.execute('SELECT COALESCE(SUM(total), 0) as total FROM sales').fetchone()['total'] or 0
    
    # Get recent sales
    recent_sales = conn.execute('''
        SELECT s.*, p.brand, p.model
        FROM sales s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.date DESC
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_products=total_products,
                         total_sales=total_sales,
                         total_customers=total_customers,
                         total_revenue=total_revenue,
                         recent_sales=recent_sales)

# Products management
@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    
    if search_query:
        # Search products by brand or model
        products = conn.execute('''
            SELECT * FROM products 
            WHERE brand LIKE ? OR model LIKE ? 
            ORDER BY created_at DESC
        ''', (f'%{search_query}%', f'%{search_query}%')).fetchall()
    else:
        # Get all products
        products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    
    conn.close()
    
    return render_template('products.html', products=products, search_query=search_query)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        
        conn = get_db_connection()
        conn.execute('INSERT INTO products (brand, model, price, quantity) VALUES (?, ?, ?, ?)',
                    (brand, model, price, quantity))
        conn.commit()
        conn.close()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        
        conn.execute('UPDATE products SET brand = ?, model = ?, price = ?, quantity = ? WHERE id = ?',
                    (brand, model, price, quantity, id))
        conn.commit()
        conn.close()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Customers management
@app.route('/customers')
def customers():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    
    if search_query:
        # Search customers by name, phone, or address
        customers = conn.execute('''
            SELECT * FROM customers 
            WHERE name LIKE ? OR phone LIKE ? OR address LIKE ? 
            ORDER BY created_at DESC
        ''', (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')).fetchall()
    else:
        # Get all customers
        customers = conn.execute('SELECT * FROM customers ORDER BY created_at DESC').fetchall()
    
    conn.close()
    
    return render_template('customers.html', customers=customers, search_query=search_query)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form.get('address', '')
        
        conn = get_db_connection()
        conn.execute('INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)',
                    (name, phone, address))
        conn.commit()
        conn.close()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('add_customer.html')

@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form.get('address', '')
        
        conn.execute('UPDATE customers SET name = ?, phone = ?, address = ? WHERE id = ?', 
                    (name, phone, address, id))
        conn.commit()
        conn.close()
        
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers'))
    
    conn.close()
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<int:id>')
def delete_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Check if customer has any sales before deleting
    sales_count = conn.execute('SELECT COUNT(*) FROM sales WHERE customer_id = ?', (id,)).fetchone()[0]
    
    if sales_count > 0:
        flash('Cannot delete customer! Customer has sales records.', 'error')
    else:
        conn.execute('DELETE FROM customers WHERE id = ?', (id,))
        conn.commit()
        flash('Customer deleted successfully!', 'success')
    
    conn.close()
    return redirect(url_for('customers'))

# Billing system
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE quantity > 0 ORDER BY brand, model').fetchall()
    customers = conn.execute('SELECT * FROM customers ORDER BY name').fetchall()
    
    # Get recent sales for the table
    recent_sales = conn.execute('''
        SELECT s.*, p.brand, p.model, c.name as customer_name
        FROM sales s
        JOIN products p ON s.product_id = p.id
        LEFT JOIN customers c ON s.customer_id = c.id
        ORDER BY s.sale_date DESC
        LIMIT 10
    ''').fetchall()
    conn.close()
    
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        customer_id = request.form.get('customer_id')
        
        conn = get_db_connection()
        
        # Get product details
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        
        if product and product['quantity'] >= quantity:
            total_price = product['price'] * quantity
            
            # Create sale record
            conn.execute('INSERT INTO sales (product_id, customer_id, quantity, total_price) VALUES (?, ?, ?, ?)',
                        (product_id, customer_id if customer_id else None, quantity, total_price))
            
            # Update product quantity
            new_quantity = product['quantity'] - quantity
            conn.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, product_id))
            
            conn.commit()
            conn.close()
            
            flash('Bill created successfully!', 'success')
            return redirect(url_for('billing'))
        else:
            flash('Insufficient stock!', 'error')
            conn.close()
    
    return render_template('billing.html', products=products, customers=customers, recent_sales=recent_sales)

# Reports
@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Daily sales
    daily_sales = conn.execute('''
        SELECT DATE(sale_date) as date, SUM(total_price) as total, COUNT(*) as count
        FROM sales
        WHERE DATE(sale_date) >= DATE('now', '-7 days')
        GROUP BY DATE(sale_date)
        ORDER BY date DESC
    ''').fetchall()
    
    # Monthly sales
    monthly_sales = conn.execute('''
        SELECT strftime('%Y-%m', sale_date) as month, SUM(total_price) as total, COUNT(*) as count
        FROM sales
        GROUP BY strftime('%Y-%m', sale_date)
        ORDER BY month DESC
        LIMIT 12
    ''').fetchall()
    
    # Top products
    top_products = conn.execute('''
        SELECT p.brand, p.model, SUM(s.quantity) as total_sold, SUM(s.total_price) as revenue
        FROM sales s
        JOIN products p ON s.product_id = p.id
        GROUP BY p.id
        ORDER BY total_sold DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('reports.html', 
                         daily_sales=daily_sales,
                         monthly_sales=monthly_sales,
                         top_products=top_products)

# Service Module Routes
@app.route('/service_requests')
def service_requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').strip()
    
    # Mock data for service requests
    requests = [
        {
            'id': 1,
            'customer_name': 'Rahul Sharma',
            'device_brand': 'Apple',
            'device_model': 'iPhone 13',
            'issue_type': 'Screen Damage',
            'status': 'Pending',
            'priority': 'Medium',
            'created_date': '2024-03-01 10:30:00'
        },
        {
            'id': 2,
            'customer_name': 'Priya Patel',
            'device_brand': 'Samsung',
            'device_model': 'Galaxy S22',
            'issue_type': 'Battery Issue',
            'status': 'In Progress',
            'priority': 'Low',
            'created_date': '2024-03-01 09:15:00'
        },
        {
            'id': 3,
            'customer_name': 'Amit Kumar',
            'device_brand': 'Xiaomi',
            'device_model': 'Redmi Note 12',
            'issue_type': 'Charging Problem',
            'status': 'Completed',
            'priority': 'High',
            'created_date': '2024-02-28 16:45:00'
        }
    ]
    
    # Filter based on search
    if search_query:
        requests = [r for r in requests if 
                  search_query.lower() in r['customer_name'].lower() or 
                  search_query.lower() in r['device_brand'].lower() or 
                  search_query.lower() in r['device_model'].lower() or 
                  search_query.lower() in r['issue_type'].lower()]
    
    # Count statuses
    pending_count = len([r for r in requests if r['status'] == 'Pending'])
    in_progress_count = len([r for r in requests if r['status'] == 'In Progress'])
    completed_count = len([r for r in requests if r['status'] == 'Completed'])
    total_count = len(requests)
    
    return render_template('service_requests.html', 
                           requests=requests,
                           search_query=search_query,
                           pending_count=pending_count,
                           in_progress_count=in_progress_count,
                           completed_count=completed_count,
                           total_count=total_count)

@app.route('/repairs')
def repairs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').strip()
    
    # Mock data for repairs
    repairs = [
        {
            'id': 1,
            'customer_name': 'Rahul Sharma',
            'device_brand': 'Apple',
            'device_model': 'iPhone 13',
            'issue_type': 'Screen Damage',
            'technician_name': 'John Doe',
            'status': 'In Progress',
            'progress': 65,
            'start_date': '2024-03-01 11:00:00'
        },
        {
            'id': 2,
            'customer_name': 'Priya Patel',
            'device_brand': 'Samsung',
            'device_model': 'Galaxy S22',
            'issue_type': 'Battery Issue',
            'technician_name': 'Jane Smith',
            'status': 'Waiting Parts',
            'progress': 30,
            'start_date': '2024-03-01 10:00:00'
        }
    ]
    
    # Filter based on search
    if search_query:
        repairs = [r for r in repairs if 
                  search_query.lower() in r['customer_name'].lower() or 
                  search_query.lower() in r['device_brand'].lower() or 
                  search_query.lower() in r['device_model'].lower() or 
                  (r['technician_name'] and search_query.lower() in r['technician_name'].lower())]
    
    # Count statuses
    diagnosis_count = len([r for r in repairs if r['status'] == 'Diagnosis'])
    in_progress_count = len([r for r in repairs if r['status'] == 'In Progress'])
    waiting_parts_count = len([r for r in repairs if r['status'] == 'Waiting Parts'])
    completed_count = len([r for r in repairs if r['status'] == 'Completed'])
    
    return render_template('repairs.html', 
                           repairs=repairs,
                           search_query=search_query,
                           diagnosis_count=diagnosis_count,
                           in_progress_count=in_progress_count,
                           waiting_parts_count=waiting_parts_count,
                           completed_count=completed_count,
                           pending_requests=[],
                           technicians=[])

@app.route('/service_history')
def service_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').strip()
    status_filter = request.args.get('status_filter', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Mock data for service history
    services = [
        {
            'id': 1,
            'service_date': '2024-02-28 15:30:00',
            'customer_name': 'Amit Kumar',
            'device_brand': 'Xiaomi',
            'device_model': 'Redmi Note 12',
            'service_type': 'Screen Replacement',
            'technician_name': 'John Doe',
            'total_cost': 2500.00,
            'status': 'Completed',
            'rating': 5
        },
        {
            'id': 2,
            'service_date': '2024-02-25 11:20:00',
            'customer_name': 'Sunita Verma',
            'device_brand': 'OPPO',
            'device_model': 'Reno 8',
            'service_type': 'Battery Replacement',
            'technician_name': 'Jane Smith',
            'total_cost': 1800.00,
            'status': 'Completed',
            'rating': 4
        }
    ]
    
    # Filter based on search
    if search_query:
        services = [s for s in services if 
                  search_query.lower() in s['customer_name'].lower() or 
                  search_query.lower() in s['device_brand'].lower() or 
                  search_query.lower() in s['device_model'].lower()]
    
    # Filter by status
    if status_filter:
        services = [s for s in services if s['status'] == status_filter]
    
    # Calculate summary stats
    total_services = len(services)
    completed_services = len([s for s in services if s['status'] == 'Completed'])
    total_revenue = sum(s['total_cost'] for s in services)
    ratings = [s['rating'] for s in services if s['rating']]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return render_template('service_history.html', 
                           services=services,
                           search_query=search_query,
                           status_filter=status_filter,
                           date_from=date_from,
                           date_to=date_to,
                           total_services=total_services,
                           completed_services=completed_services,
                           total_revenue=total_revenue,
                           avg_rating=avg_rating,
                           current_page=1,
                           total_pages=1)

@app.route('/technicians')
def technicians():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').strip()
    
    # Mock data for technicians
    technicians = [
        {
            'id': 1,
            'name': 'John Doe',
            'phone': '9876543210',
            'email': 'john@example.com',
            'specialization': 'Hardware Repair',
            'experience': 5,
            'skills': ['iPhone Repair', 'Samsung Repair', 'Soldering'],
            'status': 'Active',
            'rating': 4.5,
            'current_jobs': 2
        },
        {
            'id': 2,
            'name': 'Jane Smith',
            'phone': '9876543211',
            'email': 'jane@example.com',
            'specialization': 'Software Issues',
            'experience': 3,
            'skills': ['Android OS', 'iOS Troubleshooting', 'Data Recovery'],
            'status': 'Busy',
            'rating': 4.8,
            'current_jobs': 3
        },
        {
            'id': 3,
            'name': 'Mike Wilson',
            'phone': '9876543212',
            'email': 'mike@example.com',
            'specialization': 'Screen Replacement',
            'experience': 7,
            'skills': ['Screen Replacement', 'Glass Repair', 'LCD Repair'],
            'status': 'Active',
            'rating': 4.2,
            'current_jobs': 1
        }
    ]
    
    # Filter based on search
    if search_query:
        technicians = [t for t in technicians if 
                      search_query.lower() in t['name'].lower() or 
                      search_query.lower() in t['specialization'].lower() or 
                      search_query.lower() in t['phone'].lower() or
                      any(search_query.lower() in skill.lower() for skill in t['skills'])]
    
    # Count statuses
    total_technicians = len(technicians)
    active_technicians = len([t for t in technicians if t['status'] == 'Active'])
    busy_technicians = len([t for t in technicians if t['status'] == 'Busy'])
    available_technicians = len([t for t in technicians if t['status'] == 'Active' and t['current_jobs'] < 3])
    
    return render_template('technicians.html', 
                           technicians=technicians,
                           search_query=search_query,
                           total_technicians=total_technicians,
                           active_technicians=active_technicians,
                           busy_technicians=busy_technicians,
                           available_technicians=available_technicians)

# Shop Pages Routes
@app.route('/mobiles')
def mobiles():
    return render_template('mobiles.html')

@app.route('/shop-mobiles')
def shop_mobiles():
    return render_template('shop_mobiles.html')

@app.route('/accessories')
def accessories():
    return render_template('accessories.html')

@app.route('/basic-service')
def basic_service():
    return render_template('basic_service.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/edit-profile')
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('edit-profile.html')

@app.route('/saved-address')
def saved_address():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('saved-address.html')

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('orders.html')

@app.route('/chip-level-service')
def chip_level_service():
    return render_template('chip_level_service.html')

@app.route('/service-booking')
def service_booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('service_booking.html')

# API endpoint for user service booking
@app.route('/api/book_service', methods=['POST'])
def api_book_service():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    data = request.get_json()
    print(f"DEBUG - Received data: {data}")  # Debug logging
    
    try:
        conn = get_db_connection()
        
        # Insert service booking into database
        conn.execute('''
            INSERT INTO services (
                customer_name, phone, service_type, device_details, 
                issue_description, status, created_at
            ) VALUES (?, ?, ?, ?, ?, 'Pending', CURRENT_TIMESTAMP)
        ''', (
            data.get('fullName', ''),
            data.get('mobileNumber', ''),
            data.get('service_name', ''),
            f"{data.get('mobileBrand', '')} {data.get('modelName', '')} ({data.get('phoneColor', '')})",
            f"Condition: {data.get('phoneCondition', '')}\nProblem started: {data.get('problemStart', '')}\nPhysical damage: {data.get('physicalDamage', '')}\nPhone turning on: {data.get('turningOn', '')}\nBack cover: {data.get('backCover', '')}\nSIM card: {data.get('simCard', '')}\nMemory card: {data.get('memoryCard', '')}\nIssue: {data.get('issueDescription', '')}"
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Service booked successfully'
        }), 200
        
    except Exception as e:
        print(f"DEBUG - Error: {e}")  # Debug logging
        return jsonify({'error': str(e)}), 500

@app.route('/users')
def users():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template("users.html", data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
