class Book:
    def __init__(self, title, author, quantity=1):
        self.title = title
        self.author = author
        self.status = 'available'
        self.total_quantity = quantity
        self.quantity = quantity

    def borrow(self):
        if hasattr(self, "available"):
            if self.available > 0:
                return True
            return False
        if self.quantity > 0:
            return True
        return False

    def reserve(self):
        if hasattr(self, "available"):
            if self.available > 0 and self.status in ('available', 'borrowed'):
                self.status = 'reserved'
                return True
            return False
        if self.quantity > 0 and self.status in ('available', 'borrowed'):
            self.status = 'reserved'
            return True
        return False

    def return_book(self):
        self.status = 'available'

    def __eq__(self, other):
        return isinstance(other, Book) and (self.title, self.author) == (other.title, other.author)

    def __hash__(self):
        return hash((self.title, self.author))


