from service.library_service import LibraryService
from repository.BookRepository import BookRepository
from repository.UserRepository import UserRepository

class LibraryController:
    def __init__(self,
                 books_repo: BookRepository = BookRepository(),
                 users_repo: UserRepository = UserRepository()):
        self.service = LibraryService(books_repo, users_repo)
        self.books = books_repo
        self.users = users_repo

    def register_user(self, name):
        return self.service.register_user(name)

    def add_media(self, media_type, title, author, quantity=1):
        return self.service.add_media(media_type, title, author, quantity)

    def list_media(self):
        return self.service.list_media()

    def borrow(self, user_name, title):
        return self.service.execute("borrow", user_name, title)

    def reserve(self, user_name, title):
        return self.service.execute("reserve", user_name, title)

    def cancel(self, user_name, title):
        return self.service.execute("cancel", user_name, title)

    def return_media(self, user_name, title):
        return self.service.execute("return", user_name, title)

    def remove_media(self, title):
        return self.books.remove_by_title(title)
