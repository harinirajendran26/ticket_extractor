import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "orders.db")


def create_database():
    conn = sqlite3.connect(DB_PATH)          # creates orders.db if it doesn't exist
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("""
        CREATE TABLE orders (
            order_id    TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            product     TEXT NOT NULL,
            status      TEXT NOT NULL,
            amount      REAL NOT NULL,
            ordered_on  TEXT NOT NULL
        )
    """)

    orders = [
        ("OD123", "C1", "Wireless headphones", "shipped",   2499.0, "2026-10-01"),
        ("OD124", "C1", "Running shoes",       "delivered", 3199.0, "2026-09-20"),
        ("OD200", "C2", "Washing machine",     "placed",   28999.0, "2026-10-08"),
        ("OD201", "C2", "Glass water bottle",  "delivered",  599.0, "2026-10-02"),
        ("OD999", "C3", "Laptop",              "cancelled", 54999.0, "2026-09-15"),
    ]
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", orders)

    conn.commit()
    conn.close()
    print(f"Created {DB_PATH} with {len(orders)} orders")


if __name__ == "__main__":
    create_database()