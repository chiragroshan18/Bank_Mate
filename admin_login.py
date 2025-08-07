# admin_login.py
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import bcrypt
import logging
from exception_handler import install_exception_handler

class AdminLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        install_exception_handler()
        self.setWindowTitle("Admin Login - Bank Mate")
        self.resize(500, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF1D0;
                font-family: 'Verdana';
            }
            .login-box {
                background-color: white;
                border-radius: 15px;
                padding: 40px;
                border: 3px solid #FFB347;
            }
            QLabel {
                color: #2d3436;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #74b9ff;
                border-radius: 8px;
                font-size: 14px;
                min-width: 250px;
                background: white;
            }
            QPushButton {
                padding: 12px;
                font-size: 14px;
                min-width: 250px;
                border-radius: 8px;
                margin: 8px 0;
                border: none;
                font-weight: bold;
            }
            #title {
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
                margin-bottom: 10px;
            }
            #logo {
                margin-bottom: 20px;
            }
            #login_btn {
                background: #3498db;
                color: white;
            }
            #login_btn:hover {
                background: #2980b9;
            }
            #register_btn {
                background: #2ecc71;
                color: white;
            }
            #register_btn:hover {
                background: #27ae60;
            }
            #back_btn {
                background: #636e72;
                color: white;
            }
            #back_btn:hover {
                background: #2d3436;
            }
            #footer {
                color: #555;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        # Main login box container
        login_box = QWidget()
        login_box.setObjectName("login-box")
        box_layout = QVBoxLayout(login_box)
        box_layout.setContentsMargins(30, 30, 30, 30)
        box_layout.setSpacing(20)

        # Logo
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(QPixmap("logo.png").scaled(100, 100, 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Admin Login")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Username Input
        lbl_user = QLabel("Username:")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter admin username")

        # Password Input
        lbl_pass = QLabel("Password:")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        # Buttons
        btn_login = QPushButton("Login")
        btn_login.setObjectName("login_btn")
        btn_login.clicked.connect(self.login)

        btn_register = QPushButton("Create New Admin")
        btn_register.setObjectName("register_btn")
        btn_register.clicked.connect(self.open_register_admin)

        btn_back = QPushButton("← Back to Main Menu")
        btn_back.setObjectName("back_btn")
        btn_back.clicked.connect(self.go_back)

        # Footer
        footer = QLabel("© Chirag - Bank Mate 2025")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)

        # Assemble login box
        box_layout.addWidget(logo)
        box_layout.addWidget(title)
        box_layout.addWidget(lbl_user)
        box_layout.addWidget(self.user_input)
        box_layout.addWidget(lbl_pass)
        box_layout.addWidget(self.pass_input)
        box_layout.addWidget(btn_login)
        box_layout.addWidget(btn_register)
        box_layout.addWidget(btn_back)

        # Assemble main layout
        main_layout.addStretch()
        main_layout.addWidget(login_box)
        main_layout.addStretch()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return

        try:
            from db_config import get_db_connection
            conn, cursor = get_db_connection()
            
            cursor.execute("SELECT password_hash FROM admins WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode(), result[0].encode()):
                QMessageBox.information(self, "Success", "Login successful!")
                from admin_dashboard import AdminDashboard
                self.dashboard = AdminDashboard(username)
                self.dashboard.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials")

        except Exception as e:
            logging.error(f"Admin login error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def open_register_admin(self):
        from register_admin import AdminRegisterWindow
        self.register_window = AdminRegisterWindow()
        self.register_window.show()
        self.close()

    def go_back(self):
        from main import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = AdminLoginWindow()
    window.show()
    sys.exit(app.exec_())
