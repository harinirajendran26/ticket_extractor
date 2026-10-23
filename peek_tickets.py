import sqlite3

conn = sqlite3.connect("orders.db")
for row in conn.execute("SELECT ticket_id, customer_id, order_id, route, text FROM tickets"):
    print(row)
conn.close()