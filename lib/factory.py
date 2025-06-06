from model.book import Book
from model.audiobook import Audiobook
from lib.proxy import BookProxy

class MediaFactory:
    _registry = {}

    @classmethod
    def register(cls, media_type: str, ctor):
        cls._registry[media_type] = ctor

    @classmethod
    def create_media(cls, media_type: str, title: str, author: str, quantity=1):
        try:
            return cls._registry[media_type](title, author, quantity)
        except KeyError:
            raise ValueError(f"Unknown media type: {media_type}")

    def save(self, book):
        format_value = getattr(book, "format", None)
        self.conn.execute(
            "INSERT OR IGNORE INTO books(title,author,status,quantity,format) VALUES(?,?,?,?,?)",
            (book.title, book.author, book.status, book.quantity, format_value)
        )
        self.conn.commit()

MediaFactory.register("book", BookProxy)
MediaFactory.register("audiobook", Audiobook)