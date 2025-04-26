import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from Views.LogIn import Ui_MainWindow as LOGIN

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from Controllers.LogIn_Controller import LoginController
from socket_server import SocketServer


class LogIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LOGIN()
        self.ui.setupUi(self)
        self.ui.PasswordInput.setEchoMode(QLineEdit.Password)
        self.controller = LoginController(self)

        # Initialize and start socket server
        self.socket_server = SocketServer()
        self.socket_server.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LogIn()
    login_window.show()
    sys.exit(app.exec_())