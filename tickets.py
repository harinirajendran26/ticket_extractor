import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.environ.get("DB_PATH", "orders.db")


def init_tickets_table() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            order_id    TEXT,
            text        TEXT NOT NULL,
            route       TEXT NOT NULL,
            reason      TEXT NOT NULL,
            created_at  TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_ticket(customer_id: str, order_id: str | None, text: str,
                route: str, reason: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "INSERT INTO tickets (customer_id, order_id, text, route, reason, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (customer_id, order_id, text, route, reason,
         datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    ticket_id = cur.lastrowid
    conn.close()
    return ticket_id


def count_previous_tickets(customer_id: str, order_id: str) -> int:
    """How many earlier tickets did THIS customer raise about THIS order?"""
    conn = sqlite3.connect(DB_PATH)
    (count,) = conn.execute(
        "SELECT COUNT(*) FROM tickets WHERE customer_id = ? AND order_id = ?",
        (customer_id, order_id),
    ).fetchone()
    conn.close()
    return count


if __name__ == "__main__":
    init_tickets_table()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tickets")          # start the demo from an empty table
    conn.commit()
    conn.close()

    print("before any ticket:", count_previous_tickets("C1", "OD123"))
    save_ticket("C1", "OD123", "Where is my order?", "auto_reply", "status question")
    print("after one ticket: ", count_previous_tickets("C1", "OD123"))
    save_ticket("C1", "OD123", "Still nothing, where is it?", "human", "repeat")
    print("after two tickets:", count_previous_tickets("C1", "OD123"))
    print("same order, other customer:", count_previous_tickets("C2", "OD123"))
    print("same customer, other order:", count_previous_tickets("C1", "OD124"))