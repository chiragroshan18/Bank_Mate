# withdraw_window
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QDoubleValidator
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bank_withdraw.log'
)

class WithdrawWorker(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self, acc_no, amount):
        super().__init__()
        self.acc_no = acc_no
        self.amount = amount

    def run(self):
        try:
            from db_config import get_db_connection
            conn, cursor = get_db_connection()
            
            # Check balance first
            cursor.execute("SELECT balance FROM users WHERE account_no = %s", (self.acc_no,))
            balance = cursor.fetchone()[0]
            
            if balance < self.amount:
                raise ValueError("Insufficient balance")
                
            cursor.execute("UPDATE users SET balance = balance - %s WHERE account_no = %s",
                         (self.amount, self.acc_no))
            
            cursor.execute("INSERT INTO transactions (account_no, type, amount) VALUES (%s, 'Withdraw', %s)",
                         (self.acc_no, self.amount))
            
            conn.commit()
            self.finished.emit(True, f"Withdrew ₹{self.amount:,.2f} successfully")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

class WithdrawWindow(QWidget):
    def __init__(self, account_no):
        super().__init__()
        self.account_no = account_no
        self.setWindowTitle("Withdraw - Bank Mate")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
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
                padding: 10px;
                border: 2px solid #FFB347;
                border-radius: 5px;
                font-size: 14px;
                min-width: 250px;
            }
            QPushButton {
                padding: 12px;
                font-weight: bold;
                font-size: 16px;
                min-width: 250px;
                border-radius: 6px;
                margin: 5px;
            }
            #title {
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
            }
            #logo {
                margin-bottom: 20px;
            }
            #withdraw_btn {
                background-color: #E74C3C;
                color: white;
            }
            #back_btn {
                background-color: #FFB347;
                color: #000;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)

        # Logo
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(QPixmap("logo.png").scaled(120, 120, 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("💸 Withdraw Money")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Account Verification
        lbl_acc = QLabel("Verify Your Account Number:")
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter your account number")

        # Amount Input
        lbl_amount = QLabel("Amount to Withdraw:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("₹0.00")
        self.amount_input.setValidator(QDoubleValidator(0, 1000000, 2))

        # Buttons
        btn_withdraw = QPushButton("CONFIRM WITHDRAWAL")
        btn_withdraw.setObjectName("withdraw_btn")
        btn_withdraw.clicked.connect(self.verify_and_withdraw)
        
        btn_back = QPushButton("← BACK TO DASHBOARD")
        btn_back.setObjectName("back_btn")
        btn_back.clicked.connect(self.close_and_return)

        # Footer
        footer = QLabel("© Chirag")
        footer.setStyleSheet("""
            color: #555;
            font-size: 12px;
            font-weight: bold;
            padding-top: 20px;
        """)
        footer.setAlignment(Qt.AlignRight)

        # Assembly
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(lbl_acc)
        layout.addWidget(self.acc_input)
        layout.addWidget(lbl_amount)
        layout.addWidget(self.amount_input)
        layout.addWidget(btn_withdraw)
        layout.addWidget(btn_back)
        layout.addStretch()
        layout.addWidget(footer)

        self.setLayout(layout)

    def verify_and_withdraw(self):
        entered_acc = self.acc_input.text().strip()
        if entered_acc != self.account_no:
            QMessageBox.warning(self, "Error", "Account number doesn't match!")
            return
            
        amount_text = self.amount_input.text().strip()
        if not amount_text:
            QMessageBox.warning(self, "Error", "Please enter an amount")
            return
            
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError("Amount must be positive")
                
            self.worker = WithdrawWorker(self.account_no, amount)
            self.worker.finished.connect(self.handle_result)
            self.worker.start()
            
            QMessageBox.information(self, "Processing", "Your withdrawal is being processed...")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Amount", str(e))

    def handle_result(self, success, message):
        if success:
            QMessageBox.information(self, "Success", message)
            self.close_and_return()
        else:
            QMessageBox.critical(self, "Error", message)

    def close_and_return(self):
        from user_dashboard import UserDashboard
        self.dashboard = UserDashboard(self.account_no)
        self.dashboard.show()
        self.close()
