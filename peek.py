import sqlite3

conn = sqlite3.connect("orders.db")
cur = conn.cursor()

cur.execute("SELECT product, amount FROM orders WHERE status = 'delivered'")

for row in cur.fetchall():
    print(row)

conn.close()