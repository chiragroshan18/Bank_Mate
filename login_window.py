#login_window
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QDoubleValidator, QFont
from PyQt5.QtCore import Qt
import bcrypt
from exception_handler import install_exception_handler
import logging


install_exception_handler()

class LoginWindow(QWidget):
    """
    A login window for the Bank Mate application, styled with colorful buttons.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank Mate - Login")
        self.resize(600, 500)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface of the login window with a styled layout.
        """
        
        self.setStyleSheet("""
            QWidget { 
                background-color: #FFF1D0; 
                font-family: 'Verdana'; 
            }
            QLabel { 
                color: #333333; 
                font-size: 16px; 
            }
            QLineEdit {
                padding: 12px; 
                border: 2px solid #FFB347; 
                border-radius: 8px;
                font-size: 14px; 
                min-width: 280px; 
                background: white;
            }
            QPushButton {
                padding: 14px; 
                font-weight: bold; 
                font-size: 16px;
                min-width: 280px; 
                border-radius: 8px; 
                margin: 8px 0; 
                border: none;
                /* Add a subtle shadow to make the buttons pop out */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            #title { 
                font-size: 28px; 
                font-weight: bold; 
                color: #2C3E50; 
            }
            #login_btn { 
                background-color: #3498DB; 
                color: white; 
            }
            #login_btn:hover { 
                background-color: #2980B9; 
            }
            #register_btn { 
                background-color: #2ECC71; 
                color: white; 
            }
            #register_btn:hover { 
                background-color: #27AE60; 
            }
            #back_btn { 
                background-color: #FFB347; 
                color: #000; 
            }
            #back_btn:hover { 
                background-color: #FFA500; 
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(15)

        # Logo and Title
        logo = QLabel()
        logo.setPixmap(QPixmap("logo.png").scaled(100, 100, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Bank Mate Login")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Verdana", 28, QFont.Bold))

        # Input 
        lbl_acc = QLabel("Enter Your Account Number:")
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("e.g. 1234567890")
        self.account_input.setValidator(QDoubleValidator(0, 9999999999, 0))

        lbl_pin = QLabel("Enter Your PIN:")
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("4-digit PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setValidator(QDoubleValidator(0, 9999, 0))

        # Buttons 
        btn_login = QPushButton("LOGIN")
        btn_login.setObjectName("login_btn")
        btn_login.clicked.connect(self.login)

        btn_register = QPushButton("CREATE NEW ACCOUNT")
        btn_register.setObjectName("register_btn")
        btn_register.clicked.connect(self.open_register_window)

        btn_back = QPushButton("← BACK TO MAIN MENU")
        btn_back.setObjectName("back_btn")
        btn_back.clicked.connect(self.go_back)

        footer = QLabel("© Chirag - Bank Mate 2025")
        footer.setAlignment(Qt.AlignCenter)

        # Add widgets 
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addSpacing(20) 
        layout.addWidget(lbl_acc)
        layout.addWidget(self.account_input)
        layout.addWidget(lbl_pin)
        layout.addWidget(self.pin_input)
        layout.addWidget(btn_login)
        layout.addWidget(btn_register)
        layout.addWidget(btn_back)
        layout.addStretch()
        layout.addWidget(footer)

        self.setLayout(layout)

    def login(self):
        """
        Handles the user login process by validating credentials.
        """
        acc_no = self.account_input.text().strip()
        pin = self.pin_input.text().strip()

        if not acc_no or not pin:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            from db_config import get_db_connection
            conn, cursor = get_db_connection()
            
            cursor.execute("SELECT pin_hash FROM users WHERE account_no = %s", (acc_no,))
            result = cursor.fetchone()

            if result:
                stored_hash = result[0].encode('utf-8')
                if bcrypt.checkpw(pin.encode('utf-8'), stored_hash):
                    QMessageBox.information(self, "Success", "Login Successful!")
                    from user_dashboard import UserDashboard
                    self.dashboard = UserDashboard(acc_no)
                    self.dashboard.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Error", "Incorrect PIN")
            else:
                QMessageBox.warning(self, "Error", "Account not found")

        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def open_register_window(self):
        """
        Opens the registration window and closes the current one.
        """
        from register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def go_back(self):
        """
        Returns to the main menu and closes the current window.
        """
        from main import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
