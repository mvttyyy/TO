from model.book import Book

class Audiobook(Book):
    def __init__(self, title, author, quantity=1):
        super().__init__(title, author, quantity)
        self.format = 'audio'
