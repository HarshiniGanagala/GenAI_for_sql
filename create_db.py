
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON")

# Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
)
""")

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product TEXT,
    amount REAL,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
""")

# Sample Indian customers
customers = [
    (1, "Rahul Sharma", "rahul@gmail.com", "Mumbai"),
    (2, "Priya Reddy", "priya@gmail.com", "Hyderabad"),
    (3, "Arjun Kumar", "arjun@gmail.com", "Bangalore"),
    (4, "Sneha Patel", "sneha@gmail.com", "Delhi"),
    (5, "Kiran Rao", "kiran@gmail.com", "Chennai")
]

# Sample orders
orders = [
    (101, 1, "Laptop", 65000, "2026-10-01"),
    (102, 2, "Phone", 25000, "2026-10-02"),
    (103, 3, "Tablet", 18000, "2026-10-03"),
    (104, 4, "Laptop", 72000, "2026-10-04"),
    (105, 5, "Phone", 22000, "2026-10-05"),
    (106, 1, "Headphones", 3000, "2026-10-06"),
    (107, 2, "Tablet", 20000, "2026-10-07"),
    (108, 3, "Keyboard", 2500, "2026-10-08"),
    (109, 4, "Mouse", 1200, "2026-10-09"),
    (110, 5, "Monitor", 15000, "2026-10-10")
]

# Delete old orders first to respect foreign keys
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM customers")

# Insert or replace customer records
cursor.executemany("""
INSERT OR REPLACE INTO customers
(id, name, email, city)
VALUES (?, ?, ?, ?)
""", customers)

# Insert or replace order records
cursor.executemany("""
INSERT OR REPLACE INTO orders
(id, customer_id, product, amount, order_date)
VALUES (?, ?, ?, ?, ?)
""", orders)

# Commit changes
conn.commit()

# Verify records
cursor.execute("SELECT COUNT(*) FROM customers")
customer_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM orders")
order_count = cursor.fetchone()[0]

print("Database created successfully!")
print(f"Customers inserted: {customer_count}")
print(f"Orders inserted: {order_count}")

conn.close()
