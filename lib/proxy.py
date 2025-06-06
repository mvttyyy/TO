from model.book import Book

class BookProxy(Book):
    def __init__(self, title, author, quantity=1):
        super().__init__(title, author, quantity)
        self._real_book = None

    def _load_book(self):
        if self._real_book is None:
            print(f"Loading book '{self.title}' from storage...")
            self._real_book = Book(self.title, self.author, self.quantity)

    def get_real_book(self):
        self._load_book()
        return self._real_book

    def __getattr__(self, name):
        return getattr(self.get_real_book(), name)