from lib.db import init_db
from controller.librarycontroller import LibraryController
from view.consoleview import ConsoleView

def main():
    init_db()
    ctrl = LibraryController()
    view = ConsoleView()

    # przykładowa inicjalizacja
    ctrl.register_user("Ola")
    ctrl.register_user("Tomek")
    ctrl.add_media("book", "Wiedźmin", "A. Sapkowski")
    ctrl.add_media("audiobook", "Mistrz i Małgorzata", "M. Bułhakow")

    # Paginacja przy pierwszym wyświetleniu
    books = ctrl.books.all()
    page = 0
    page_size = 10
    while True:
        try:
            view.show_media_page(books, page, page_size)
        except AttributeError:
            view.show_media_list(books)
        nav = view.prompt("Sterowanie ([n]/[p]/[q] powrót do menu): ")
        if nav == "n" and page < (len(books) - 1) // page_size:
            page += 1
        elif nav == "p" and page > 0:
            page -= 1
        elif nav == "q":
            break

    # Główne menu operacji
    while True:
        books = ctrl.books.all()
        view.show_media_list(books)
        cmd = view.prompt("\nKomenda (borrow/reserve/return/quit): ")
        if cmd == "quit":
            break
        if cmd not in ("borrow", "reserve", "return"):
            view.show_message(f"Nieznana komenda: {cmd}")
            continue

        user = view.prompt("Użytkownik: ")
        idx = view.prompt_index("Wybierz numer pozycji: ", len(books))
        title = books[idx].title

        method = "return_media" if cmd == "return" else cmd
        try:
            success = getattr(ctrl, method)(user, title)
            view.show_message("OK" if success else "Nie powiodło się")
        except Exception as e:
            view.show_message(f"Błąd: {e}")

if __name__ == "__main__":
    main()