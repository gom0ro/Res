import sqlite3
import sys

# Force utf-8 output encoding for print
sys.stdout.reconfigure(encoding='utf-8')

def check_db():
    conn = sqlite3.connect('resort.db')
    cursor = conn.cursor()
    
    print("--- ORDERS ---")
    cursor.execute("SELECT * FROM orders")
    for r in cursor.fetchall():
        print(repr(r))
        
    print("\n--- ORDER ITEMS ---")
    cursor.execute("SELECT * FROM order_items")
    for r in cursor.fetchall():
        print(repr(r))
        
    conn.close()

if __name__ == '__main__':
    check_db()
