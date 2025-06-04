from repository.interfaces import IBookRepository, IUserRepository
from lib.factory import MediaFactory
from model.user import User

class LibraryService:
    def __init__(self, books: IBookRepository, users: IUserRepository):
        self.books = books
        self.users = users
        # command registry for OCP
        self._actions = {}
        self.register_action("borrow",   self._do_borrow)
        self.register_action("reserve",  self._do_reserve)
        self.register_action("return",   self._do_return)
        self.register_action("cancel",   self._do_cancel)

    def register_action(self, name: str, handler):
        """Allow external registration of new commands."""
        self._actions[name] = handler

    def execute(self, cmd: str, user_name: str, title: str):
        if cmd not in self._actions:
            return False, f"Nieznana operacja '{cmd}'"
        return self._actions[cmd](user_name, title)

    def register_user(self, name: str):
        user = User(name)
        self.users.save(user)
        return True, f"Użytkownik '{name}' zarejestrowany"

    def add_media(self, media_type: str, title: str, author: str):
        media = MediaFactory.create_media(media_type, title, author)
        self.books.save(media)
        return media

    def list_media(self):
        return self.books.all()

    def _do_borrow(self, user_name: str, title: str):
        user = self.users.find_by_name(user_name)
        book = self.books.find_by_title(title)
        if book.status == 'available' or (book.status == 'reserved' and book in user.reserved):
            book.borrow()
            self.books.update(book)
            self.users.add_borrow(user_name, title)
            if book in user.reserved:
                user.reserved.remove(book)
                self.users.remove_reserve(user_name, title)
            return True, f"'{title}' wypożyczono przez {user_name}"
        return False, f"Książka '{title}' jest obecnie {book.status}"

    def _do_reserve(self, user_name: str, title: str):
        user = self.users.find_by_name(user_name)
        if not user:
            return False, f"Nie znaleziono użytkownika '{user_name}'"
        book = self.books.find_by_title(title)
        if not book:
            return False, f"Nie znaleziono pozycji '{title}'"
        if not book.reserve():
            return False, f"Nie można zarezerwować '{title}' (status: {book.status})"
        book.add_observer(user)
        self.books.update(book)
        self.users.add_reserve(user_name, title)
        return True, f"'{title}' zarezerwowano przez {user_name}"

    def _do_return(self, user_name: str, title: str):
        user = self.users.find_by_name(user_name)
        if not user:
            return False, f"Nie znaleziono użytkownika '{user_name}'"
        book = self.books.find_by_title(title)
        if not book:
            return False, f"Nie znaleziono pozycji '{title}'"
        if book not in user.borrowed:
            return False, f"Książka '{title}' nie była wypożyczona przez {user_name}"
        book.return_book()
        self.books.update(book)
        self.users.remove_borrow(user_name, title)
        return True, f"'{title}' zwrócono przez {user_name}"

    def _do_cancel(self, user_name: str, title: str):
        user = self.users.find_by_name(user_name)
        book = self.books.find_by_title(title)
        if not user or not book or book not in user.reserved:
            return False, f"Brak rezerwacji '{title}' przez {user_name}"
        # usuń rezerwację w DB i lokalnie
        self.users.remove_reserve(user_name, title)
        user.cancel_reservation(book)
        # zwolnij status książki
        book.status = 'available'
        self.books.update(book)
        return True, f"Rezerwacja '{title}' anulowana przez {user_name}"