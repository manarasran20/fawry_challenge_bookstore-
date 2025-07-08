from datetime import datetime


class Book:
    def __init__(self, isbn, title, year, price):
        self.isbn = isbn
        self.title = title
        self.year = year
        self.price = price

    def buy(self, qty, email, address):
        raise NotImplementedError("buy() should be implemented")


class PaperBook(Book):
    def __init__(self, isbn, title, year, price, stock):
        super().__init__(isbn, title, year, price)
        self.stock = stock

    def buy(self, qty, email, address):
        if self.stock < qty:
            raise Exception("Insufficient stock for paper book.")
        self.stock -= qty
        print(f"[Shipping] '{self.title}' sent to {address}")
        return self.price * qty


class EeBook(Book):
    def __init__(self, isbn, title, year, price, filetype):
        super().__init__(isbn, title, year, price)
        self.filetype = filetype

    def buy(self, qty, email, address):
        print(f"[Email] '{self.title}' sent to {email} as a {self.filetype} file")
        return self.price * qty


class ShowcaseBook(Book):
    def __init__(self, isbn, title, year):
        super().__init__(isbn, title, year, 0)

    def buy(self, qty, email, address):
        raise Exception("This book is only for display purposes.")


class Store:
    def __init__(self):
        self.books = {}
    def add(self, book):
        self.books[book.isbn] = book
        print(f"[Added] {book.title}")
    def remove_old(self, max_years):
        now = datetime.now().year
        gone = []
        for isbn in list(self.books.keys()):
            age = now - self.books[isbn].year
            if age > max_years:
                gone.append(self.books[isbn].title)
                del self.books[isbn]
        print(f"[Removed outdated] {gone}")
    def buy(self, isbn, qty, email, address):
        if isbn not in self.books:
            print("Book not found.")
            return
        try:
            paid = self.books[isbn].buy(qty, email, address)
            print(f"[Success] Paid: ${paid}")
        except Exception as e:
            print("[Failed]", str(e))


#testing
def try_store():
    s = Store()
    b1 = PaperBook("001", "Python in Depth", 2020, 120, 5)
    b2 = EeBook("002", "Learn AI Fast", 2023, 60, "epub")
    b3 = ShowcaseBook("003", "The Rare One", 1900)
    s.add(b1)
    s.add(b2)
    s.add(b3)
    s.buy("001", 2, "manar@site.com", "Giza 10")
    s.buy("002", 1, "manar@site.com", "")
    s.buy("003", 1, "manar@site.com", "Giza 10")
    s.remove_old(50)
    print("Remaining inventory:", list(s.books.keys()))
try_store()
