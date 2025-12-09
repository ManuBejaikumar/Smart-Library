class Book:
    def __init__(self, book_id, title, isbn, category, publication_year, copies_available):
        self.book_id = book_id
        self.title = title
        self.isbn = isbn
        self.category = category
        self.publication_year = publication_year
        self.copies_available = copies_available