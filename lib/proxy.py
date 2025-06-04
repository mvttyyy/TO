from model.book import Book

class BookProxy(Book):
    def __init__(self, title, author):
        super().__init__(title, author)
        self._real_book = None

    def _load_book(self):
        if self._real_book is None:
            print(f"Loading book '{self.title}' from storage...")
            # load fresh Book instance
            self._real_book = Book(self.title, self.author)

    def get_real_book(self):
        self._load_book()
        return self._real_book

    def __getattr__(self, name):
        # forward any missing attribute calls to real Book
        return getattr(self.get_real_book(), name)