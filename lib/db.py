import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'library.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
      CREATE TABLE IF NOT EXISTS users(
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
      )
    """)
    c.execute("""
      CREATE TABLE IF NOT EXISTS books(
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        title  TEXT    UNIQUE NOT NULL,
        author TEXT            NOT NULL,
        status TEXT            NOT NULL
      )
    """)
    c.execute("""
      CREATE TABLE IF NOT EXISTS borrowed(
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(book_id) REFERENCES books(id),
        UNIQUE(user_id, book_id)
      )
    """)
    c.execute("""
      CREATE TABLE IF NOT EXISTS reserved(
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(book_id) REFERENCES books(id),
        UNIQUE(user_id, book_id)
      )
    """)
    conn.commit()
    conn.close()