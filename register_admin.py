# register_admin.py
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import bcrypt

class AdminRegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Admin - Bank Mate")
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF1D0;
                font-family: 'Verdana';
            }
            QLabel {
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #74b9ff;
                border-radius: 5px;
                font-size: 14px;
                min-width: 250px;
                background: white;
            }
            QPushButton {
                padding: 12px;
                font-size: 14px;
                min-width: 250px;
                border-radius: 5px;
                margin: 8px 0;
                border: none;
            }
            #title {
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
            }
            #logo {
                margin-bottom: 10px;
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

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(15)

        # Logo
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(QPixmap("logo.png").scaled(100, 100, 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Register New Admin")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Username Input
        lbl_user = QLabel("Username:")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter new username")

        # Password Input
        lbl_pass = QLabel("Password:")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        # Buttons
        btn_register = QPushButton("Register")
        btn_register.setObjectName("register_btn")
        btn_register.clicked.connect(self.register_admin)

        btn_back = QPushButton("← Back to Login")  
        btn_back.setObjectName("back_btn")
        btn_back.clicked.connect(self.go_back)

        # Footer
        footer = QLabel("© Chirag")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignRight)

        # Assembly
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(lbl_user)
        layout.addWidget(self.user_input)
        layout.addWidget(lbl_pass)
        layout.addWidget(self.pass_input)
        layout.addWidget(btn_register)
        layout.addWidget(btn_back)
        layout.addStretch()
        layout.addWidget(footer)

        self.setLayout(layout)

    def register_admin(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return

        try:
            from db_config import get_db_connection
            conn, cursor = get_db_connection()
            
            # Check if admin exists
            cursor.execute("SELECT 1 FROM admins WHERE username = %s", (username,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Error", "Username already exists")
                return

            # Hash password and create admin
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO admins (username, password_hash) VALUES (%s, %s)",
                (username, hashed_pw.decode())
            )
            conn.commit()
            
            QMessageBox.information(self, "Success", "Admin registered successfully!")
            self.go_back()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def go_back(self):
        from admin_login import AdminLoginWindow
        self.login_window = AdminLoginWindow()
        self.login_window.show()
        self.close()
