import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'resort.db')
print(f"Connecting to database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check and add 'color' column
try:
    cursor.execute("ALTER TABLE bar_categories ADD COLUMN color TEXT")
    print("Added column 'color' to 'bar_categories'")
except sqlite3.OperationalError as e:
    print(f"Column 'color' might already exist: {e}")

# Check and add 'icon' column
try:
    cursor.execute("ALTER TABLE bar_categories ADD COLUMN icon TEXT")
    print("Added column 'icon' to 'bar_categories'")
except sqlite3.OperationalError as e:
    print(f"Column 'icon' might already exist: {e}")

# Check and add 'position' column
try:
    cursor.execute("ALTER TABLE bar_categories ADD COLUMN position INTEGER DEFAULT 0")
    print("Added column 'position' to 'bar_categories'")
except sqlite3.OperationalError as e:
    print(f"Column 'position' might already exist: {e}")

# Let's initialize default categories with some colors/icons and positions
default_categories = {
    "Общее": ("#4B5563", "🍽️", 0),  # gray, plate
    "Напитки": ("#3B82F6", "🥤", 1), # blue, drink
    "Закуски": ("#F59E0B", "🍿", 2)  # amber, snack
}

for name, (color, icon, position) in default_categories.items():
    cursor.execute(
        "UPDATE bar_categories SET color = ?, icon = ?, position = ? WHERE name = ?",
        (color, icon, position, name)
    )
    print(f"Initialized attributes for default category '{name}'")

conn.commit()
conn.close()
print("Migration completed successfully.")
