#!/usr/bin/env python3
"""
Initialize accessory stock database
Run this script to populate the admin dashboard with all accessory products
"""

import sqlite3
import os

# Database path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def init_accessory_stock():
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
    
    # Define all accessory products from accessories.html with 20 quantity
    accessories_data = [
        # Cases (10 products)
        ('Mobile Engineer', 'Premium Phone Case - iPhone 15', 999, 20),
        ('Mobile Engineer', 'Leather Phone Case - Samsung Galaxy S24', 1299, 20),
        ('Mobile Engineer', 'Silicone Phone Case - Redmi Note 13 Pro', 699, 20),
        ('Mobile Engineer', 'Clear Phone Case - OnePlus 12', 799, 20),
        ('Mobile Engineer', 'Wallet Phone Case - Google Pixel 8', 1499, 20),
        ('Mobile Engineer', 'Armored Phone Case - Realme 11 Pro', 1199, 20),
        ('Mobile Engineer', 'Gel Phone Case - Poco X6 Pro', 599, 20),
        ('Mobile Engineer', 'Ring Phone Case - Vivo X100', 899, 20),
        ('Mobile Engineer', 'Book Phone Case - Oppo Find X7', 1099, 20),
        ('Mobile Engineer', 'Metal Phone Case - Nothing Phone 2', 1399, 20),
        # Chargers (9 products)
        ('Mobile Engineer', 'Fast Charger', 1499, 20),
        ('Mobile Engineer', 'Wireless Charger', 2499, 20),
        ('Mobile Engineer', 'Car Charger', 899, 20),
        ('Mobile Engineer', 'Wall Charger', 1299, 20),
        ('Mobile Engineer', 'Multi-Port Charger', 2999, 20),
        ('Mobile Engineer', 'USB Hub Charger', 1799, 20),
        ('Mobile Engineer', 'MagSafe Charger', 3499, 20),
        ('Mobile Engineer', 'Portable Charger', 1999, 20),
        ('Mobile Engineer', 'Solar Charger', 4999, 20),
        # Headphones (9 products)
        ('Mobile Engineer', 'Wireless Headphones', 2999, 20),
        ('Mobile Engineer', 'Over-Ear Headphones', 4999, 20),
        ('Mobile Engineer', 'In-Ear Headphones', 1999, 20),
        ('Mobile Engineer', 'Gaming Headphones', 3499, 20),
        ('Mobile Engineer', 'Noise Canceling Headphones', 5999, 20),
        ('Mobile Engineer', 'Wireless Earbuds', 2499, 20),
        ('Mobile Engineer', 'Sports Headphones', 1799, 20),
        ('Mobile Engineer', 'Studio Headphones', 6999, 20),
        ('Mobile Engineer', 'Kids Headphones', 1299, 20),
        # Screen Protectors (9 products)
        ('Mobile Engineer', 'Tempered Glass Screen Protector - Redmi Note 9 Pro', 499, 20),
        ('Mobile Engineer', 'Privacy Screen Protector - Samsung Galaxy S24 Ultra', 799, 20),
        ('Mobile Engineer', 'Matte Screen Protector - iPhone 15 Pro Max', 599, 20),
        ('Mobile Engineer', 'HD Screen Protector - OnePlus 12', 699, 20),
        ('Mobile Engineer', 'Anti-Blue Light Screen Protector - Google Pixel 8 Pro', 899, 20),
        ('Mobile Engineer', 'Curved Screen Protector - Realme 11 Pro', 999, 20),
        ('Mobile Engineer', 'Hydrogel Screen Protector - Vivo X100', 399, 20),
        ('Mobile Engineer', 'Camera Lens Protector - Oppo Find X7', 299, 20),
        ('Mobile Engineer', 'Full Coverage Screen Protector - Nothing Phone 2', 1199, 20),
        # Power Banks (9 products)
        ('Mobile Engineer', 'Power Bank 10000mAh', 1999, 20),
        ('Mobile Engineer', 'Power Bank 20000mAh', 2999, 20),
        ('Mobile Engineer', 'Wireless Power Bank', 3499, 20),
        ('Mobile Engineer', 'Slim Power Bank', 1499, 20),
        ('Mobile Engineer', 'High Capacity Power Bank', 4999, 20),
        ('Mobile Engineer', 'Solar Power Bank', 5999, 20),
        ('Mobile Engineer', 'Magnetic Power Bank', 2799, 20),
        ('Mobile Engineer', 'Portable Power Station', 9999, 20),
        ('Mobile Engineer', 'Quick Charge Power Bank', 2499, 20),
    ]
    
    # Clear existing accessory products
    print("Clearing existing accessory products...")
    cursor.execute('DELETE FROM products WHERE category = "accessory"')
    deleted = cursor.rowcount
    print(f"Deleted {deleted} existing accessory products")
    
    # Insert all accessory products
    print("Inserting accessory products...")
    inserted_count = 0
    for brand, model, price, quantity in accessories_data:
        try:
            cursor.execute(
                'INSERT INTO products (brand, model, price, quantity, category) VALUES (?, ?, ?, ?, ?)',
                (brand, model, price, quantity, 'accessory')
            )
            inserted_count += 1
            print(f"  Added: {brand} {model}")
        except Exception as e:
            print(f"  Error adding {brand} {model}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"SUCCESS! Added {inserted_count} accessory products")
    print(f"Each product has 20 units in stock")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Initializing accessory stock database...\n")
    init_accessory_stock()
    print("\nDone! Refresh your admin dashboard to see the accessory stock.")
