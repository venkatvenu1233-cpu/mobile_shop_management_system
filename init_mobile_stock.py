#!/usr/bin/env python3
"""
Initialize mobile stock database
Run this script to populate the admin dashboard with all mobile products
"""

import sqlite3
import os

# Database path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def init_mobile_stock():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if category column exists
    cursor.execute("PRAGMA table_info(products)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add category column if it doesn't exist
    if 'category' not in columns:
        print("Adding category column to products table...")
        cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "mobile"')
        conn.commit()
        print("Category column added!")
    
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
    
    # Clear existing mobile products
    print("Clearing existing mobile products...")
    cursor.execute('DELETE FROM products WHERE category = "mobile" OR category IS NULL')
    deleted = cursor.rowcount
    print(f"Deleted {deleted} existing mobile products")
    
    # Insert all mobile products
    print("Inserting mobile products...")
    inserted_count = 0
    for brand, model, price, quantity in mobiles_data:
        try:
            cursor.execute(
                'INSERT INTO products (brand, model, price, quantity, category) VALUES (?, ?, ?, ?, ?)',
                (brand, model, price, quantity, 'mobile')
            )
            inserted_count += 1
            print(f"  Added: {brand} {model}")
        except Exception as e:
            print(f"  Error adding {brand} {model}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"SUCCESS! Added {inserted_count} mobile products")
    print(f"Each product has 10 units in stock")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Initializing mobile stock database...\n")
    init_mobile_stock()
    print("\nDone! Refresh your admin dashboard to see the mobile stock.")
