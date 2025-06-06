class User:
    def __init__(self, name):
        self.name = name
        self.borrowed = []
        self.reserved = []

    def borrow_book(self, book):
        if not book:
            print("Błąd: Nie znaleziono książki.")
            return
        if book.borrow():
            self.borrowed.append(book)
            print(f"{self.name} borrowed '{book.title}'")
        else:
            print(f"{self.name} could not borrow '{book.title}'")

    def return_book(self, book):
        if not book:
            print("Błąd: Nie znaleziono książki.")
            return
        if book in self.borrowed:
            self.borrowed.remove(book)
            book.return_book()
            print(f"{self.name} returned '{book.title}'")
        else:
            print(f"{self.name} nie wypożyczył(a) '{book.title}'")

    def reserve_book(self, book):
        if not book:
            print("Błąd: Nie znaleziono książki.")
            return
        if book.reserve():
            self.reserved.append(book)
            print(f"{self.name} reserved '{book.title}'")
        else:
            print(f"{self.name} could not reserve '{book.title}'")

    def cancel_reservation(self, book):
        if not book:
            print("Błąd: Nie znaleziono książki.")
            return
        if book in self.reserved:
            self.reserved.remove(book)
            print(f"{self.name} canceled reservation for '{book.title}'")
        else:
            print(f"{self.name} nie miał(a) rezerwacji na '{book.title}'")
