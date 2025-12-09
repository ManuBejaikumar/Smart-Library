from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, \
    QSpinBox
from DAO.BookDAO import BookDAO
from DAO.AuthorDAO import AuthorDAO


class BookManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Title")
        layout.addWidget(self.title_input)

        self.isbn_input = QLineEdit(self)
        self.isbn_input.setPlaceholderText("ISBN")
        layout.addWidget(self.isbn_input)

        self.category_input = QLineEdit(self)
        self.category_input.setPlaceholderText("Category")
        layout.addWidget(self.category_input)

        self.year_input = QSpinBox(self)
        self.year_input.setRange(1000, 2100)
        self.year_input.setValue(2023)
        layout.addWidget(self.year_input)

        self.copies_input = QSpinBox(self)
        self.copies_input.setRange(1, 100)
        self.copies_input.setValue(1)
        layout.addWidget(self.copies_input)

        self.author_id_input = QLineEdit(self)
        self.author_id_input.setPlaceholderText("Author IDs (comma-separated)")
        layout.addWidget(self.author_id_input)

        add_btn = QPushButton("Add Book", self)
        add_btn.clicked.connect(self.add_book)
        layout.addWidget(add_btn)

        self.book_table = QTableWidget(0, 5)
        self.book_table.setHorizontalHeaderLabels(["ID", "Title", "ISBN", "Category", "Available"])
        layout.addWidget(self.book_table)

        self.setLayout(layout)
        self.load_books()

    def load_books(self):
        books = BookDAO().get_all()
        self.book_table.setRowCount(len(books))
        for i, book in enumerate(books):
            self.book_table.setItem(i, 0, QTableWidgetItem(str(book.book_id)))
            self.book_table.setItem(i, 1, QTableWidgetItem(book.title))
            self.book_table.setItem(i, 2, QTableWidgetItem(book.isbn or ""))
            self.book_table.setItem(i, 3, QTableWidgetItem(book.category or ""))
            self.book_table.setItem(i, 4, QTableWidgetItem(str(book.copies_available)))

    def add_book(self):
        title = self.title_input.text()
        isbn = self.isbn_input.text()
        category = self.category_input.text()
        year = self.year_input.value()
        copies = self.copies_input.value()
        author_ids = [int(a.strip()) for a in self.author_id_input.text().split(',') if a.strip()]

        if BookDAO().add_book(title, isbn, category, year, copies, author_ids):
            QMessageBox.information(self, "Success", "Book added!")
            self.load_books()
        else:
            QMessageBox.warning(self, "Error", "Failed to add book.")