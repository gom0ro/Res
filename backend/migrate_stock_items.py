import sqlite3
import os

db_path = "resort.db"
if not os.path.exists(db_path):
    # fallback to check in parent/child directories
    db_path = os.path.join(os.path.dirname(__file__), "resort.db")

print(f"Connecting to database at: {os.path.abspath(db_path)}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Create table stock_items if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    stock_quantity REAL DEFAULT 0.0,
    unit TEXT DEFAULT 'кг',
    price REAL DEFAULT 0.0,
    is_active INTEGER DEFAULT 1
)
""")

# 2. Seed stock_items with raw ingredients
ingredients = [
    ("Помидоры", 45.0, "кг", 450.0),
    ("Огурцы", 30.0, "кг", 350.0),
    ("Мясо филе (Говядина)", 80.0, "кг", 3200.0),
    ("Мясо филе (Курица)", 120.0, "кг", 1800.0),
    ("Фрукты (Апельсины, Лимоны)", 60.0, "кг", 800.0),
    ("Ягоды (Клубника, Малина)", 15.0, "кг", 2500.0),
    ("Картофель", 200.0, "кг", 200.0),
    ("Зелень (Укроп, Петрушка)", 10.0, "кг", 1500.0),
    ("Сливки & Молоко", 90.0, "л", 650.0),
    ("Сиропы в ассортименте", 35.0, "шт", 1200.0),
    ("Coca-Cola 0.5", 100.0, "шт", 300.0),
    ("Fanta 0.5", 100.0, "шт", 300.0),
    ("Чипсы Lays", 50.0, "шт", 500.0),
    ("Пиво Разливное 0.5", 200.0, "шт", 600.0),
]

for name, qty, unit, price in ingredients:
    try:
        cursor.execute(
            "INSERT INTO stock_items (name, stock_quantity, unit, price, is_active) VALUES (?, ?, ?, ?, 1)",
            (name, qty, unit, price)
        )
        print(f"Seeded ingredient: {name}")
    except sqlite3.IntegrityError:
        print(f"Ingredient already exists: {name}")
        pass

# 3. Truncate stock_receipts so that receipts correctly reference the new ingredients table
try:
    cursor.execute("DELETE FROM stock_receipts")
    print("Cleared legacy stock receipts to avoid foreign key violations.")
except Exception as e:
    print(f"Note on stock receipts: {e}")

conn.commit()
conn.close()
print("Database migrated and seeded successfully!")
