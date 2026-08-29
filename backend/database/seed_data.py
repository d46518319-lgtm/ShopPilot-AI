import sqlite3
import os
from datetime import datetime, timedelta
import random

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'shoppilot.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Run the schema file to create tables
    with open(SCHEMA_PATH, 'r') as f:
        cursor.executescript(f.read())

    print("Tables created.")

    # ---------- CUSTOMERS ----------
    first_names = ['Aarav', 'Vivaan', 'Aditi', 'Diya', 'Kabir', 'Ananya', 'Ishaan', 'Myra', 'Reyansh', 'Saanvi']
    last_names = ['Sharma', 'Verma', 'Patel', 'Gupta', 'Reddy', 'Nair', 'Iyer', 'Singh', 'Rao', 'Mehta']

    customers = []
    for i in range(50):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        name = f"{fname} {lname}"
        email = f"{fname.lower()}.{lname.lower()}{i}@example.com"
        signup_date = (datetime.now() - timedelta(days=random.randint(10, 365))).strftime('%Y-%m-%d')
        customers.append((name, email, signup_date))

    cursor.executemany(
        "INSERT INTO customers (name, email, signup_date) VALUES (?, ?, ?)",
        customers
    )
    print(f"Inserted {len(customers)} customers.")

    # ---------- PRODUCTS ----------
    products = [
        ("Running Shoes", 2499.0, 40, 8420),
        ("Yoga Mat", 899.0, 60, 5200),
        ("Water Bottle", 399.0, 100, 3100),
        ("Wireless Earbuds", 3499.0, 25, 9200),
        ("Backpack", 1899.0, 35, 4100),
        ("Smart Watch", 5999.0, 15, 7600),
        ("Denim Jacket", 2199.0, 20, 2900),
        ("Sunglasses", 799.0, 50, 3600),
        ("Laptop Sleeve", 699.0, 45, 1800),
        ("Bluetooth Speaker", 1999.0, 30, 4700),
    ]
    cursor.executemany(
        "INSERT INTO products (name, price, stock, views) VALUES (?, ?, ?, ?)",
        products
    )
    print(f"Inserted {len(products)} products.")

    # ---------- ORDERS + ORDER_ITEMS ----------
    order_count = 0
    for _ in range(150):
        customer_id = random.randint(1, 50)
        order_date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')

        num_items = random.randint(1, 3)
        chosen_products = random.sample(range(1, 11), num_items)
        total = 0
        items_to_insert = []

        for product_id in chosen_products:
            price = products[product_id - 1][1]
            quantity = random.randint(1, 2)
            total += price * quantity
            items_to_insert.append((product_id, quantity, price))

        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, total_amount) VALUES (?, ?, ?)",
            (customer_id, order_date, round(total, 2))
        )
        order_id = cursor.lastrowid

        for product_id, quantity, price in items_to_insert:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )
        order_count += 1

    print(f"Inserted {order_count} orders with items.")

    # ---------- CART_ITEMS (abandoned carts) ----------
    cart_count = 0
    for _ in range(40):
        customer_id = random.randint(1, 50)
        product_id = random.randint(1, 10)
        added_date = (datetime.now() - timedelta(days=random.randint(0, 14))).strftime('%Y-%m-%d')
        cursor.execute(
            "INSERT INTO cart_items (customer_id, product_id, added_date) VALUES (?, ?, ?)",
            (customer_id, product_id, added_date)
        )
        cart_count += 1

    print(f"Inserted {cart_count} cart items (abandoned carts).")

    conn.commit()
    conn.close()
    print("\nDatabase seeded successfully at:", DB_PATH)

if __name__ == "__main__":
    create_database()