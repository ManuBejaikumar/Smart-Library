from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, \
    QTextEdit
from DAO.BookClubDAO import BookClubDAO


class BookClubWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        layout = QVBoxLayout()

        if self.current_user.role == 'member':
            self.name_input = QLineEdit(self)
            self.name_input.setPlaceholderText("Club Name")
            layout.addWidget(self.name_input)

            self.desc_input = QTextEdit(self)
            self.desc_input.setPlaceholderText("Description")
            layout.addWidget(self.desc_input)

            create_btn = QPushButton("Create Club", self)
            create_btn.clicked.connect(self.create_club)
            layout.addWidget(create_btn)

        self.club_table = QTableWidget(0, 3)
        self.club_table.setHorizontalHeaderLabels(["ID", "Name", "Description"])
        layout.addWidget(self.club_table)

        join_btn = QPushButton("Join Selected Club", self)
        join_btn.clicked.connect(self.join_club)
        layout.addWidget(join_btn)

        self.setLayout(layout)
        self.load_clubs()

    def load_clubs(self):
        clubs = BookClubDAO().get_all()
        self.club_table.setRowCount(len(clubs))
        for i, club in enumerate(clubs):
            self.club_table.setItem(i, 0, QTableWidgetItem(str(club.club_id)))
            self.club_table.setItem(i, 1, QTableWidgetItem(club.name))
            self.club_table.setItem(i, 2, QTableWidgetItem(club.description or ""))

    def create_club(self):
        name = self.name_input.text()
        desc = self.desc_input.toPlainText()
        if BookClubDAO().create_club(name, desc, self.current_user.user_id):
            QMessageBox.information(self, "Success", "Club created!")
            self.load_clubs()
        else:
            QMessageBox.warning(self, "Error", "Failed to create club.")

    def join_club(self):
        selected = self.club_table.currentRow()
        if selected >= 0:
            club_id = int(self.club_table.item(selected, 0).text())
            if BookClubDAO().join_club(club_id, self.current_user.user_id):
                QMessageBox.information(self, "Success", "Joined club!")
            else:
                QMessageBox.warning(self, "Error", "Failed to join or already member.")