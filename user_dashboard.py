# user_dashboard.py
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, 
                            QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from exception_handler import install_exception_handler

class UserDashboard(QWidget):  
    """
    A dashboard for logged-in users to access various banking features.
    """
    def __init__(self, account_no):
        super().__init__()
        install_exception_handler()
        self.account_no = account_no
        self.setWindowTitle(f"User Dashboard - Account {account_no}")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface with colorful feature boxes and a styled layout.
        """
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF1D0;
                font-family: 'Verdana';
            }
            #title {
                font-size: 28px;
                font-weight: bold;
                color: #2C3E50;
                margin: 20px 0;
            }
            #logo {
                margin-bottom: 20px;
            }
            #footer {
                color: #555;
                font-size: 12px;
                font-weight: bold;
                padding-top: 20px;
            }
            /* Enhanced styling for the feature boxes */
            .feature-box {
                background-color: white;
                border-radius: 10px;
                padding: 30px; /* Increased padding for a larger box */
                margin: 10px;
                min-width: 200px;
                border: 3px solid;
                /* Add a subtle box-shadow to make it pop */
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            /* Specific hover effect for the boxes */
            .feature-box:hover {
                transform: scale(1.05); /* Slightly enlarge the box on hover */
                transition: transform 0.2s ease-in-out;
            }

            /* Consistent styling for the Logout button */
            QPushButton#logout_btn {
                background-color: #9b59b6;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 16px;
                min-width: 200px;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            QPushButton#logout_btn:hover {
                background-color: #8e44ad;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        # Main Logo at the top
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(QPixmap("logo.png").scaled(120, 120, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel(f"Welcome, Account {self.account_no}")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        
        # Feature Boxes Container
        features_container = QWidget()
        features_container.setStyleSheet("background: transparent;")
        features_layout = QHBoxLayout(features_container)
        features_layout.setSpacing(30)
        features_layout.setAlignment(Qt.AlignCenter)

        # Create colorful feature boxes with their specific icons and colors
        withdraw_box = self.create_feature_box("💸 Withdraw", "#e74c3c", self.open_withdraw)
        deposit_box = self.create_feature_box("💰 Deposit", "#2ecc71", self.open_deposit)
        history_box = self.create_feature_box("📊 History", "#3498db", self.open_history)

        features_layout.addWidget(withdraw_box)
        features_layout.addWidget(deposit_box)
        features_layout.addWidget(history_box)

        # Logout Button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setObjectName("logout_btn")
        logout_btn.clicked.connect(self.logout)

        # Footer
        footer = QLabel("© Chirag")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignRight)

        # Assemble all components
        main_layout.addWidget(logo)
        main_layout.addWidget(title)
        main_layout.addWidget(features_container)
        main_layout.addWidget(logout_btn, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def create_feature_box(self, text, color, callback):
        """
        Helper method to create a clickable feature box widget.
        """
        box = QWidget()
        box.setObjectName("feature-box")
        box.setStyleSheet(f"border-color: {color};")
        
        layout = QVBoxLayout(box)
        layout.setAlignment(Qt.AlignCenter)
        
        # The icon is the first part of the text string (e.g., "💸")
        icon = QLabel(text.split()[0])
        icon.setStyleSheet(f"font-size: 32px;") 
        
        # The label is the rest of the text (e.g., "Withdraw")
        label = QLabel(" ".join(text.split()[1:]))
        label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 18px;")
        
        layout.addWidget(icon)
        layout.addWidget(label)
        
        # Make the entire box clickable by connecting its mousePressEvent
        box.mousePressEvent = lambda event: callback()
        return box

    def open_withdraw(self):
        """
        Opens the withdrawal window.
        """
        from withdraw_window import WithdrawWindow
        self.withdraw_window = WithdrawWindow(self.account_no)
        self.withdraw_window.show()
        self.close()

    def open_deposit(self):
        """
        Opens the deposit window.
        """
        from deposit_window import DepositWindow
        self.deposit_window = DepositWindow(self.account_no)
        self.deposit_window.show()
        self.close()

    def open_history(self):
        """
        Opens the transaction history window.
        """
        from transaction_history import TransactionHistory
        self.history_window = TransactionHistory(self.account_no)
        self.history_window.show()
        self.close()

    def logout(self):
        """
        Logs the user out and returns to the main menu.
        """
        from main import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
