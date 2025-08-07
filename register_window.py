# register_window.py
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QPixmap, QIntValidator, QFont
from PyQt5.QtCore import Qt
import bcrypt

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank Mate - Register")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF1D0;
                font-family: 'Verdana';
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #FFB347;
                border-radius: 5px;
                font-size: 14px;
                min-width: 250px;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
                min-width: 250px;
                border-radius: 5px;
                margin: 5px 0;
            }
            #register_btn {
                background: #4CAF50;
                color: white;
            }
            #back_btn {
                background: #FFB347;
                color: black;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(15)

        # Logo
        logo = QLabel()
        logo.setPixmap(QPixmap("logo.png").scaled(100, 100, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Create New Account")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        # Input Fields
        lbl_name = QLabel("Full Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")

        lbl_acc = QLabel("Account Number:")
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("e.g. 1234")
        self.acc_input.setValidator(QIntValidator(1, 999999999))

        lbl_pin = QLabel("4-digit PIN:")
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("4 digits")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setValidator(QIntValidator(1000, 9999))

        # Buttons
        btn_register = QPushButton("Register", self)
        btn_register.setObjectName("register_btn")
        btn_register.clicked.connect(self.register_user)

        btn_back = QPushButton("Back to Login", self)
        btn_back.setObjectName("back_btn")
        btn_back.clicked.connect(self.go_back)

        # Footer (made bolder)
        footer = QLabel("© Chirag")
        footer.setFont(QFont('Verdana', 10, QFont.Bold))  
        footer.setStyleSheet("color: #555;")
        footer.setAlignment(Qt.AlignRight)

        # Add widgets to layout
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(lbl_name)
        layout.addWidget(self.name_input)
        layout.addWidget(lbl_acc)
        layout.addWidget(self.acc_input)
        layout.addWidget(lbl_pin)
        layout.addWidget(self.pin_input)
        layout.addWidget(btn_register)
        layout.addWidget(btn_back)
        layout.addStretch()
        layout.addWidget(footer)

        self.setLayout(layout)

    def register_user(self):
        name = self.name_input.text().strip()
        acc_no = self.acc_input.text().strip()
        pin = self.pin_input.text().strip()

        if not name or not acc_no or not pin:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if len(pin) != 4:
            QMessageBox.warning(self, "Error", "PIN must be 4 digits!")
            return

        try:
            from db_config import get_db_connection
            conn, cursor = get_db_connection()
            
            # Check if account exists
            cursor.execute("SELECT 1 FROM users WHERE account_no = %s", (acc_no,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Error", "Account already exists!")
                return

            # Hash PIN and create account
            hashed_pin = bcrypt.hashpw(pin.encode(), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (name, account_no, pin_hash, balance) VALUES (%s, %s, %s, 0)",
                (name, acc_no, hashed_pin.decode())
            )
            conn.commit()
            
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.go_back()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def go_back(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
