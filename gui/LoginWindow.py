from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

from DAO.UserDAO import UserDAO


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.user = None
        self.setWindowTitle("SmartLibrary Login")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login", self)
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_dao = UserDAO()
        user = user_dao.authenticate(username, password)
        if user:
            self.accept()
            self.user = user
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")