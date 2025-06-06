from lib.db import init_db
from controller.librarycontroller import LibraryController
from view.consoleview import ConsoleView

def main():
    init_db()
    ctrl = LibraryController()
    view = ConsoleView()

    ctrl.register_user("Ola")
    ctrl.register_user("Tomek")

    media_to_seed = [
        ("book", "Wiedźmin", "A. Sapkowski"),
        ("audiobook", "Mistrz i Małgorzata", "M. Bułhakow"),
        ("book", "Pan Tadeusz", "Adam Mickiewicz"),
        ("book", "Rok 1984", "George Orwell"),
        ("book", "Zbrodnia i kara", "Fiodor Dostojewski"),
        ("book", "Harry Potter i Kamień Filozoficzny", "J.K. Rowling"),
        ("book", "Hobbit, czyli tam i z powrotem", "J.R.R. Tolkien"),
        ("book", "Przeminęło z wiatrem", "Margaret Mitchell"),
        ("book", "Duma i uprzedzenie", "Jane Austen"),
        ("book", "Wojna i pokój", "Lew Tołstoj"),
        ("book", "Bracia Karamazow", "Fiodor Dostojewski"),
        ("book", "Sto lat samotności", "Gabriel García Márquez"),
        ("book", "Wielki Gatsby", "F. Scott Fitzgerald"),
        ("book", "Zabić drozda", "Harper Lee"),
        ("book", "Krzyżacy", "Henryk Sienkiewicz"),
        ("audiobook", "Solaris", "Stanisław Lem"),
        ("audiobook", "Mały Książę", "Antoine de Saint-Exupéry"),
    ]
    existing = {b.title for b in ctrl.books.all()}
    for media_type, title, author in media_to_seed:
        if title not in existing:
            ctrl.add_media(media_type, title, author)

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