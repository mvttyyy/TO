# model/audiobook.py
from model.book import Book

class Audiobook(Book):
    def __init__(self, title, author):
        super().__init__(title, author)
        self.format = 'audio'
