import sqlite3
conn = sqlite3.connect("library.db")
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in library.db:", cur.fetchall())
conn.close()