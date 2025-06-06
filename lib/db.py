import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'library.db')

class SingletonDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cls._instance.conn.row_factory = sqlite3.Row
            cls._instance.conn.execute("PRAGMA foreign_keys = ON")
        return cls._instance

    def get_connection(self):
        return self.conn

def get_connection():
    return SingletonDBConnection().get_connection()

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
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        title   TEXT    UNIQUE NOT NULL,
        author  TEXT            NOT NULL,
        status  TEXT            NOT NULL,
        quantity INTEGER        NOT NULL DEFAULT 1,
        format TEXT
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