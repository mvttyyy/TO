class Book:
    def __init__(self, title, author, quantity=1):
        self.title = title
        self.author = author
        self.status = 'available'
        self.observers = []
        self.total_quantity = quantity
        self.quantity = quantity

    def borrow(self):
        if self.status in ('available', 'reserved'):
            return True
        return False

    def reserve(self):
        if self.status in ('available', 'borrowed'):
            self.status = 'reserved'
            return True
        return False

    def return_book(self):
        self.status = 'available'
        self.notify_observers()

    def add_observer(self, user):
        self.observers.append(user)

    def notify_observers(self):
        for user in self.observers:
            print(f"[NOTIFY] {user.name}, '{self.title}' is now available.")
        self.observers.clear()

    def __eq__(self, other):
        return isinstance(other, Book) and (self.title, self.author) == (other.title, other.author)

    def __hash__(self):
        return hash((self.title, self.author))


