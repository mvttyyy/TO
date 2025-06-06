import sqlite3
from lib.db import get_connection
from model.user import User
from model.book import Book
from repository.interfaces import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self):
        self.conn = get_connection()

    def save(self, user):
        self.conn.execute(
            "INSERT OR IGNORE INTO users(name) VALUES(?)",
            (user.name,)
        )
        self.conn.commit()

    def find_by_name(self, name):
        row = self.conn.execute(
            "SELECT id,name FROM users WHERE name = ?",
            (name,)
        ).fetchone()
        if not row:
            return None
        user = User(row['name'])
        user.reserved = []
        rows = self.conn.execute(
            "SELECT b.title,b.author,b.status "
            "FROM borrowed br "
            " JOIN books b ON br.book_id=b.id "
            "WHERE br.user_id=?",
            (row['id'],)
        ).fetchall()
        for r in rows:
            bk = Book(r['title'], r['author'])
            bk.status = r['status']
            user.borrowed.append(bk)
        rows2 = self.conn.execute(
            "SELECT b.title,b.author,b.status "
            "FROM reserved r "
            " JOIN books b ON r.book_id=b.id "
            "WHERE r.user_id=?",
            (row['id'],)
        ).fetchall()
        for r in rows2:
            bk = Book(r['title'], r['author'])
            bk.status = r['status']
            user.reserved.append(bk)
        return user

    def add_borrow(self, user_name, title):
        self.conn.execute(
            "INSERT OR IGNORE INTO borrowed(user_id,book_id) "
            "SELECT u.id,b.id FROM users u,books b WHERE u.name=? AND b.title=?",
            (user_name, title)
        )
        self.conn.commit()

    def remove_borrow(self, user_name, title):
        self.conn.execute(
            "DELETE FROM borrowed "
            "WHERE user_id=(SELECT id FROM users WHERE name=?) "
              "AND book_id=(SELECT id FROM books WHERE title=?)",
            (user_name, title)
        )
        self.conn.commit()

    def add_reserve(self, user_name: str, title: str):
        """Implement the interface method to insert into reserved."""
        self.conn.execute(
            "INSERT OR IGNORE INTO reserved(user_id, book_id) "
            "SELECT u.id, b.id FROM users u, books b "
            "WHERE u.name = ? AND b.title = ?",
            (user_name, title)
        )
        self.conn.commit()

    def remove_reserve(self, user_name: str, title: str):
        """Implement the interface method to delete from reserved."""
        self.conn.execute(
            "DELETE FROM reserved "
            "WHERE user_id = (SELECT id FROM users WHERE name = ?) "
              "AND book_id = (SELECT id FROM books WHERE title = ?)",
            (user_name, title)
        )
        self.conn.commit()