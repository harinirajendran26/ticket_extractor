import sqlite3

conn = sqlite3.connect("orders.db")
cur = conn.cursor()

cur.execute("SELECT product, status FROM orders WHERE customer_id = 'C1'")

for row in cur.fetchall():
    print(row)

conn.close()