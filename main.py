# main
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from exception_handler import install_exception_handler

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        install_exception_handler()
        self.setWindowTitle("Welcome to Bank Mate")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF1D0;
                font-family: 'Verdana';
            }
            .login-option {
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                margin: 20px;
                min-width: 250px;
                border: 3px solid;
            }
            .login-option:hover {
                background-color: #f5f5f5;
            }
            #title {
                font-size: 28px;
                font-weight: bold;
                color: #2C3E50;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        logo = QLabel()
        logo.setPixmap(QPixmap("logo.png").scaledToWidth(650))
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("🏦 Welcome to Bank Mate")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        options_container = QWidget()
        options_layout = QHBoxLayout(options_container)
        options_layout.setSpacing(40)
        options_layout.setAlignment(Qt.AlignCenter)

        user_option = self.create_login_option("👤 User Login", "#3498db", self.open_user_login)
        admin_option = self.create_login_option("🔒 Admin Login", "#e74c3c", self.open_admin_login)

        options_layout.addWidget(user_option)
        options_layout.addWidget(admin_option)

        footer = QLabel("© Chirag")
        footer.setStyleSheet("color: #555; font-size: 12px; font-weight: bold;")
        footer.setAlignment(Qt.AlignRight)

        main_layout.addStretch()
        main_layout.addWidget(logo)
        main_layout.addWidget(title)
        main_layout.addWidget(options_container)
        main_layout.addStretch()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def create_login_option(self, text, color, callback):
        box = QWidget()
        box.setObjectName("login-option")
        box.setStyleSheet(f"border-color: {color};")
        
        layout = QVBoxLayout(box)
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel(text.split()[0])
        icon.setStyleSheet("font-size: 36px;")
        
        label = QLabel(" ".join(text.split()[1:]))
        label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 18px;")
        
        layout.addWidget(icon)
        layout.addWidget(label)
        
        box.mousePressEvent = lambda event: callback()
        return box

    def open_user_login(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_admin_login(self):
        from admin_login import AdminLoginWindow
        self.admin_login = AdminLoginWindow()
        self.admin_login.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
