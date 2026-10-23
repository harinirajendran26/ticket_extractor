import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "orders.db")


def get_order_status(order_id: str, current_customer_id: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row            # lets us read columns by name
    try:
        row = conn.execute(
            "SELECT order_id, customer_id, product, status, amount, ordered_on "
            "FROM orders WHERE order_id = ?",
            (order_id,),
        ).fetchone()
    finally:
        conn.close()

    # Same answer whether the order doesn't exist or belongs to someone else
    if row is None or row["customer_id"] != current_customer_id:
        return {"error": "order not found"}

    return {
        "order_id": row["order_id"],
        "product": row["product"],
        "status": row["status"],
        "amount": row["amount"],
        "ordered_on": row["ordered_on"],
    }


if __name__ == "__main__":
    print(get_order_status("OD123", "C1"))   # C1's own order
    print(get_order_status("OD123", "C2"))   # someone else's order
    print(get_order_status("OD000", "C1"))   # doesn't exist