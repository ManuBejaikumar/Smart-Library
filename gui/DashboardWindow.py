# ui/DashboardWindow.py   ← REPLACE COMPLETELY
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from DAO.LoanDAO import LoanDAO
from DAO.BookDAO import BookDAO
from db_connection import get_connection

class DashboardWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        layout = QVBoxLayout()

        title = QLabel(f"Welcome, {current_user.username} ({current_user.role.capitalize()})")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        if current_user.role == 'librarian':
            self.librarian_dashboard(layout)
        else:
            self.member_dashboard(layout)

        self.setLayout(layout)

    def librarian_dashboard(self, layout):
        books = BookDAO().get_all()
        layout.addWidget(QLabel(f"Total Books in Library: {len(books)}"))


        with get_connection().cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM loans WHERE return_date IS NULL")
            active = cur.fetchone()[0]
        layout.addWidget(QLabel(f"Active Loans: {active}"))

    def member_dashboard(self, layout):

        loans = LoanDAO().get_active_loans(self.current_user.user_id)
        layout.addWidget(QLabel(f"My Active Loans: {len(loans)} / 3"))

        table = QTableWidget(len(loans), 4)
        table.setHorizontalHeaderLabels(["Loan ID", "Book ID", "Loan Date", "Due Date"])
        for i, loan in enumerate(loans):
            table.setItem(i, 0, QTableWidgetItem(str(loan.loan_id)))
            table.setItem(i, 1, QTableWidgetItem(str(loan.book_id)))
            table.setItem(i, 2, QTableWidgetItem(str(loan.loan_date)))
            table.setItem(i, 3, QTableWidgetItem(str(loan.due_date)))
        layout.addWidget(table)