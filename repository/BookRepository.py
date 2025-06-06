import sqlite3
from model.book import Book
from model.audiobook import Audiobook
from lib.db import get_connection
from repository.interfaces import IBookRepository
from lib.proxy import BookProxy

class BookRepository(IBookRepository):
    def __init__(self):
        self.conn = get_connection()

    def save(self, book):
        format_value = getattr(book, "format", None)
        self.conn.execute(
            "INSERT OR IGNORE INTO books(title,author,status,quantity,format) VALUES(?,?,?,?,?)",
            (book.title, book.author, book.status, book.quantity, format_value)
        )
        self.conn.commit()

    def update(self, book):
        self.conn.execute(
            "UPDATE books SET status = ?, quantity = ? WHERE title = ?",
            (book.status, book.quantity, book.title)
        )
        self.conn.commit()

    def find_by_title(self, title):
        row = self.conn.execute(
            "SELECT id,title,author,quantity,format FROM books WHERE title = ?",
            (title,)
        ).fetchone()
        if not row:
            return None
        if row['format'] == 'audio':
            b = Audiobook(row['title'], row['author'], row['quantity'])
        else:
            b = Book(row['title'], row['author'], row['quantity'])
        b.id = row['id']
        borrowed = self.conn.execute(
            "SELECT COUNT(*) FROM borrowed WHERE book_id=?", (b.id,)
        ).fetchone()[0]
        reserved = self.conn.execute(
            "SELECT COUNT(*) FROM reserved WHERE book_id=?", (b.id,)
        ).fetchone()[0]
        b.borrowed_count = borrowed
        b.reserved_count = reserved
        b.available = b.total_quantity - borrowed - reserved
        if borrowed > 0:
            b.status = 'borrowed'
        elif reserved > 0:
            b.status = 'reserved'
        else:
            b.status = 'available'
        return b

    def all(self):
        rows = self.conn.execute(
            "SELECT id,title FROM books"
        ).fetchall()
        result = []
        for row in rows:
            b = BookProxy(row['title'], author=None, quantity=None)
            b.id = row['id']
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