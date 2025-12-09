from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from DAO.LoanDAO import LoanDAO


class LoanManagementWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        layout = QVBoxLayout()

        self.loan_table = QTableWidget(0, 5)
        self.loan_table.setHorizontalHeaderLabels(["ID", "Book ID", "Loan Date", "Due Date", "Returned"])
        layout.addWidget(self.loan_table)

        if self.current_user.role == 'member':
            return_btn = QPushButton("Return Selected Book", self)
            return_btn.clicked.connect(self.return_book)
            layout.addWidget(return_btn)

        self.setLayout(layout)
        self.load_loans()

    def load_loans(self):
        if self.current_user.role == 'librarian':
            loans = LoanDAO().get_loans_for_member(None)  # All
        else:
            loans = LoanDAO().get_loans_for_member(self.current_user.user_id)

        self.loan_table.setRowCount(len(loans))
        for i, loan in enumerate(loans):
            self.loan_table.setItem(i, 0, QTableWidgetItem(str(loan.loan_id)))
            self.loan_table.setItem(i, 1, QTableWidgetItem(str(loan.book_id)))
            self.loan_table.setItem(i, 2, QTableWidgetItem(str(loan.loan_date)))
            self.loan_table.setItem(i, 3, QTableWidgetItem(str(loan.due_date)))
            self.loan_table.setItem(i, 4, QTableWidgetItem("Yes" if loan.return_date else "No"))

    def return_book(self):
        selected = self.loan_table.currentRow()
        if selected >= 0:
            loan_id = int(self.loan_table.item(selected, 0).text())
            if LoanDAO().return_book(loan_id):
                QMessageBox.information(self, "Success", "Book returned!")
                self.load_loans()
            else:
                QMessageBox.warning(self, "Error", "Cannot return this book.")