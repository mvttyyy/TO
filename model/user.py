class User:
    def __init__(self, name):
        self.name = name
        self.borrowed = []
        self.reserved = []

    def borrow_book(self, book):
        if book.borrow():
            self.borrowed.append(book)
            print(f"{self.name} borrowed '{book.title}'")
        else:
            print(f"{self.name} could not borrow '{book.title}' (status: {book.status})")

    def return_book(self, book):
        if book in self.borrowed:
            self.borrowed.remove(book)
            book.return_book()
            print(f"{self.name} returned '{book.title}'")

    def reserve_book(self, book):
        if book.reserve():
            book.add_observer(self)
            self.reserved.append(book)
            print(f"{self.name} reserved '{book.title}'")
        else:
            print(f"{self.name} could not reserve '{book.title}'")

    def cancel_reservation(self, book):
        if book in self.reserved:
            self.reserved.remove(book)
            print(f"{self.name} canceled reservation for '{book.title}'")
