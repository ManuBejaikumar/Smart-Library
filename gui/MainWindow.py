from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QMenuBar, QAction, QMessageBox
from PyQt5.QtCore import Qt
from gui.DashboardWindow import DashboardWindow
from gui.BookCatalogWindow import BookCatalogWindow
from gui.BookManagementWindow import BookManagementWindow
from gui.LoanManagementWindow import LoanManagementWindow
from gui.BookClubWindow import BookClubWindow


class MainWindow(QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("SmartLibrary")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.dashboard = DashboardWindow(self.current_user)
        self.book_catalog = BookCatalogWindow(self.current_user)
        self.book_management = BookManagementWindow() if self.current_user.role == 'librarian' else None
        self.loan_management = LoanManagementWindow(self.current_user)
        self.book_club = BookClubWindow(self.current_user)

        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.book_catalog)
        if self.book_management:
            self.stacked_widget.addWidget(self.book_management)
        self.stacked_widget.addWidget(self.loan_management)
        self.stacked_widget.addWidget(self.book_club)

        self.create_menu()


    def create_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        view_menu = menu_bar.addMenu("View")
        dashboard_action = QAction("Dashboard", self)
        dashboard_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard))
        view_menu.addAction(dashboard_action)

        catalog_action = QAction("Book Catalog", self)
        catalog_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.book_catalog))
        view_menu.addAction(catalog_action)

        if self.current_user.role == 'librarian':
            management_menu = menu_bar.addMenu("Management")
            book_mgmt_action = QAction("Book Management", self)
            book_mgmt_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.book_management))
            management_menu.addAction(book_mgmt_action)

        loan_action = QAction("Loans", self)
        loan_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.loan_management))
        view_menu.addAction(loan_action)

        club_action = QAction("Book Clubs", self)
        club_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.book_club))
        view_menu.addAction(club_action)