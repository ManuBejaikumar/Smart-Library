# main.py  ← REPLACE YOUR CURRENT main.py WITH THIS
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from gui.LoginWindow import LoginWindow
from gui.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginWindow()
    result = login.exec_()

    if result == QDialog.Accepted:
        print("Login successful! User:", login.user.username, login.user.role)
        try:
            main_window = MainWindow(login.user)
            main_window.show()
            sys.exit(app.exec_())
        except Exception as e:
            print("ERROR LAUNCHING MAIN WINDOW:", e)
            import traceback

            traceback.print_exc()
    else:
        print("Login cancelled")
        sys.exit(0)