import sqlite3
conn = sqlite3.connect("orders.db")
conn.execute("DELETE FROM tickets")
conn.commit()
conn.close()