import sqlite3
from model.book import Book
from lib.db import get_connection
from repository.interfaces import IBookRepository

class BookRepository(IBookRepository):
    def __init__(self):
        self.conn = get_connection()

    def save(self, book):
        # status column is now just initial, real status derived from relations
        self.conn.execute(
            "INSERT OR IGNORE INTO books(title,author) VALUES(?,?)",
            (book.title, book.author)
        )
        self.conn.commit()

    def update(self, book):
        # keep status column in sync (optional)
        self.conn.execute(
            "UPDATE books SET status = ? WHERE title = ?",
            (book.status, book.title)
        )
        self.conn.commit()

    def find_by_title(self, title):
        row = self.conn.execute(
            "SELECT id,title,author FROM books WHERE title = ?",
            (title,)
        ).fetchone()
        if not row:
            return None
        b = Book(row['title'], row['author'])
        b.id = row['id']
        # derive actual status from borrowed/reserved tables
        if self.conn.execute(
            "SELECT 1 FROM borrowed WHERE book_id=?", (b.id,)
        ).fetchone():
            b.status = 'borrowed'
        elif self.conn.execute(
            "SELECT 1 FROM reserved WHERE book_id=?", (b.id,)
        ).fetchone():
            b.status = 'reserved'
        else:
            b.status = 'available'
        return b

    def all(self):
        rows = self.conn.execute(
            "SELECT id,title,author FROM books"
        ).fetchall()
        result = []
        for row in rows:
            b = Book(row['title'], row['author'])
            b.id = row['id']
            # derive status
            if self.conn.execute(
                "SELECT 1 FROM borrowed WHERE book_id=?", (b.id,)
            ).fetchone():
                b.status = 'borrowed'
            elif self.conn.execute(
                "SELECT 1 FROM reserved WHERE book_id=?", (b.id,)
            ).fetchone():
                b.status = 'reserved'
            else:
                b.status = 'available'
            result.append(b)
        return result