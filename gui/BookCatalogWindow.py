from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from DAO.BookDAO import BookDAO
from DAO.LoanDAO import LoanDAO
from db_connection import get_connection


class BookCatalogWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search by title or author...")
        layout.addWidget(self.search_input)

        search_btn = QPushButton("Search", self)
        search_btn.clicked.connect(self.search_books)
        layout.addWidget(search_btn)

        self.book_table = QTableWidget(0, 5)
        self.book_table.setHorizontalHeaderLabels(["ID", "Title", "ISBN", "Category", "Available"])
        layout.addWidget(self.book_table)

        if self.current_user.role == 'member':
            borrow_btn = QPushButton("Borrow Selected Book", self)
            borrow_btn.clicked.connect(self.borrow_book)
            layout.addWidget(borrow_btn)

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

    def search_books(self):
        keyword = self.search_input.text()
        books = BookDAO().search(keyword)
        self.book_table.setRowCount(len(books))
        for i, book in enumerate(books):
            self.book_table.setItem(i, 0, QTableWidgetItem(str(book.book_id)))
            self.book_table.setItem(i, 1, QTableWidgetItem(book.title))
            self.book_table.setItem(i, 2, QTableWidgetItem(book.isbn or ""))
            self.book_table.setItem(i, 3, QTableWidgetItem(book.category or ""))
            self.book_table.setItem(i, 4, QTableWidgetItem(str(book.copies_available)))

    def borrow_book(self):
        selected = self.book_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Please select a book")
            return
        book_id = int(self.book_table.item(selected, 0).text())


        member_id = getattr(self.current_user, 'member_id', self.current_user.user_id)

        if LoanDAO().borrow_book(book_id, member_id):
            QMessageBox.information(self, "Success", "Book borrowed successfully!")
            self.load_books()
        else:
            QMessageBox.warning(self, "Failed", "No copies available or you already have 3 loans")