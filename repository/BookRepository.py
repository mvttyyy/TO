import sqlite3
from model.book import Book
from lib.db import get_connection
from repository.interfaces import IBookRepository

class BookRepository(IBookRepository):
    def __init__(self):
        self.conn = get_connection()

    def save(self, book):
        self.conn.execute(
            "INSERT OR IGNORE INTO books(title,author,status) VALUES(?,?,?)",
            (book.title, book.author, book.status)
        )
        self.conn.commit()

    def update(self, book):
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

    def remove_by_title(self, title):
        row = self.conn.execute(
            "SELECT id FROM books WHERE title = ?", (title,)
        ).fetchone()
        if not row:
            return False, "Nie znaleziono książki."
        book_id = row['id']
        if self.conn.execute("SELECT 1 FROM borrowed WHERE book_id=?", (book_id,)).fetchone():
            return False, "Nie można usunąć książki, która jest wypożyczona."
        if self.conn.execute("SELECT 1 FROM reserved WHERE book_id=?", (book_id,)).fetchone():
            return False, "Nie można usunąć książki, która jest zarezerwowana."
        self.conn.execute(
            "DELETE FROM books WHERE id = ?", (book_id,)
        )
        self.conn.commit()
        return True, "Książka została usunięta."