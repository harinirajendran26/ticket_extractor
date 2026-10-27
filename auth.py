import hashlib
import os
import secrets
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "orders.db")


def init_auth_tables() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            customer_id TEXT PRIMARY KEY,
            salt        TEXT NOT NULL,
            pw_hash     TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token       TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _hash(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()


def create_user(customer_id: str, password: str) -> None:
    salt = secrets.token_hex(16)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (customer_id, salt, _hash(password, salt)),
    )
    conn.commit()
    conn.close()


def login(customer_id: str, password: str) -> str | None:
    """Return a new session token if the password is right, otherwise None."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT salt, pw_hash FROM users WHERE customer_id = ?", (customer_id,)
    ).fetchone()
    if row is None or not secrets.compare_digest(_hash(password, row[0]), row[1]):
        conn.close()
        return None
    token = secrets.token_urlsafe(32)
    conn.execute("INSERT INTO sessions VALUES (?, ?)", (token, customer_id))
    conn.commit()
    conn.close()
    return token


def customer_for_token(token: str) -> str | None:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT customer_id FROM sessions WHERE token = ?", (token,)
    ).fetchone()
    conn.close()
    return row[0] if row else None