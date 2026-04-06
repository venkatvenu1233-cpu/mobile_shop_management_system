#!/usr/bin/env python3
"""
Diagnostic script to test the order API and identify HTTP 500 errors
"""
import sqlite3
import json
import sys
from datetime import datetime

print("=" * 60)
print("ORDER API DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Check database connection and tables
print("\n[TEST 1] Checking database...")
try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check if orders table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    if cursor.fetchone():
        print("✓ Orders table exists")
    else:
        print("✗ Orders table does NOT exist")
        sys.exit(1)
    
    # Check if sales table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
    if cursor.fetchone():
        print("✓ Sales table exists")
    else:
        print("✗ Sales table does NOT exist")
    
    conn.close()
    print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database error: {e}")
    sys.exit(1)

# Test 2: Simulate the order insertion logic
print("\n[TEST 2] Testing order insertion logic...")
try:
    # Test data
    test_data = {
        'order_id': 'TEST-123',
        'customer_name': 'Test User',
        'items': [
            {
                'product_id': 1,
                'name': 'Test Product',
                'brand': 'Test Brand',
                'price': 999,
                'quantity': 1
            }
        ],
        'total': 999,
        'address': '123 Test St, Test City',
        'payment_method': 'Cash on Delivery'
    }
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Test sales insertion
    customer_name = test_data.get('customer_name', 'Guest')
    items = test_data.get('items', [])
    total_amount = 0
    
    for item in items:
        product_id = item.get('product_id', 1)
        quantity = item.get('quantity', 1) or item.get('qty', 1)
        price = item.get('price', 0)
        item_total = price * quantity
        total_amount += item_total
        
        cursor.execute('''
            INSERT INTO sales (customer_name, product_id, quantity, total, date) 
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_name, product_id, quantity, item_total, 
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    print(f"✓ Sales insertion successful (inserted {len(items)} items)")
    
    # Test orders insertion
    order_id = test_data.get('order_id', '')
    address = test_data.get('address', '')
    payment_method = test_data.get('payment_method', '')
    
    cursor.execute('''
        INSERT INTO orders (order_id, customer_name, items, total, address, payment_method, date, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_id,
        customer_name,
        json.dumps(items),
        total_amount,
        address,
        payment_method,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'pending'
    ))
    
    print("✓ Orders insertion successful")
    
    # Rollback test data
    conn.rollback()
    print("✓ Test data rolled back")
    conn.close()
    
except Exception as e:
    print(f"✗ Order insertion error: {e}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

# Test 3: Check Flask app imports
print("\n[TEST 3] Checking Flask app...")
try:
    import flask
    print(f"✓ Flask version: {flask.__version__}")
    
    # Try to import json module
    import json
    print("✓ json module available")
    
    # Try to import traceback
    import traceback
    print("✓ traceback module available")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nIf you're still getting HTTP 500, the issue is likely:")
print("1. Flask server not restarted after code changes")
print("2. Server not running at all")
print("3. Different error in the route (check server console)")
print("\nRestart Flask server with: python app.py")
