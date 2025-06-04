from model.book import Book
from model.audiobook import Audiobook
from lib.proxy import BookProxy

class MediaFactory:
    _registry = {}

    @classmethod
    def register(cls, media_type: str, ctor):
        cls._registry[media_type] = ctor

    @classmethod
    def create_media(cls, media_type: str, title: str, author: str):
        try:
            return cls._registry[media_type](title, author)
        except KeyError:
            raise ValueError(f"Unknown media type: {media_type}")

# register defaults
MediaFactory.register("book", BookProxy)       # now returns a BookProxy (LSP)
MediaFactory.register("audiobook", Audiobook)