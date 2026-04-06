import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Check if orders table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
result = cursor.fetchone()

if result:
    print("Orders table exists!")
    cursor.execute('PRAGMA table_info(orders)')
    columns = cursor.fetchall()
    print('Orders table columns:')
    for col in columns:
        print(f'  - {col[1]} ({col[2]})')
else:
    print("Orders table does NOT exist!")

conn.close()
