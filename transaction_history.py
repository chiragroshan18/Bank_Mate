# transaction_history
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QFont, QBrush
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bank_transactions.log'
)

class TransactionLoader(QThread):
    loaded = pyqtSignal(list)
    
    def __init__(self, acc_no):
        super().__init__()
        self.acc_no = acc_no

    def run(self):
        try:
            from db_config import get_db_connection
            conn, cursor = get_db_connection()
            cursor.execute("""
                SELECT type, amount, timestamp 
                FROM transactions 
                WHERE account_no = %s 
                ORDER BY timestamp DESC
                LIMIT 100
            """, (self.acc_no,))
            self.loaded.emit(cursor.fetchall())
        finally:
            if 'conn' in locals():
                conn.close()

class TransactionHistory(QWidget):
    def __init__(self, account_no):
        super().__init__()
        self.account_no = account_no
        self.setWindowTitle("Transaction History - Bank Mate")
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
                margin-bottom: 10px;
            }
            #logo {
                margin-bottom: 20px;
            }
            #verify_btn {
                background-color: #3498DB;
                color: white;
            }
            #back_btn {
                background-color: #FFB347;
                color: #000;
            }
            QTableWidget {
                background-color: white;
                border: 2px solid #FFB347;
                border-radius: 8px;
                font-size: 14px;
                gridline-color: #FFB347;
            }
            QHeaderView::section {
                background-color: #FFB347;
                color: black;
                padding: 12px;
                font-weight: bold;
                font-size: 15px;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)

        # Logo and Title
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(QPixmap("logo.png").scaled(120, 120, 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("Transaction History")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Account Verification
        lbl_verify = QLabel("Verify Your Account Number:")
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter your account number")
        
        btn_verify = QPushButton("VERIFY & LOAD TRANSACTIONS")
        btn_verify.setObjectName("verify_btn")
        btn_verify.clicked.connect(self.verify_and_load)

        # Transactions Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Type", "Amount", "Date & Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        # Back Button
        btn_back = QPushButton("← BACK TO DASHBOARD")
        btn_back.setObjectName("back_btn")
        btn_back.clicked.connect(self.go_back)

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
        layout.addWidget(lbl_verify)
        layout.addWidget(self.acc_input)
        layout.addWidget(btn_verify)
        layout.addWidget(self.table)
        layout.addWidget(btn_back)
        layout.addWidget(footer)

        self.setLayout(layout)

    def verify_and_load(self):
        entered_acc = self.acc_input.text().strip()
        if entered_acc != self.account_no:
            QMessageBox.warning(self, "Error", 
                "Account number doesn't match logged-in account!")
            return
            
        self.load_transactions()

    def load_transactions(self):
        self.loader = TransactionLoader(self.account_no)
        self.loader.loaded.connect(self.display_transactions)
        self.loader.start()
        QMessageBox.information(self, "Loading", 
            "Fetching your transaction history...")

    def display_transactions(self, transactions):
        self.table.setRowCount(len(transactions))
        
        for row, (txn_type, amount, timestamp) in enumerate(transactions):
            
            type_item = QTableWidgetItem(txn_type.upper())
            type_item.setTextAlignment(Qt.AlignCenter)
            
            # Amount Column (using ₹ symbol)
            amount_str = f"₹{float(amount):,.2f}"
            amount_item = QTableWidgetItem(amount_str)
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Date Column
            date_str = datetime.strftime(timestamp, "%d %b %Y, %I:%M %p")
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            
            # Set items
            self.table.setItem(row, 0, type_item)
            self.table.setItem(row, 1, amount_item)
            self.table.setItem(row, 2, date_item)
            
            
            if txn_type == "Deposit":
                type_item.setForeground(QBrush(QColor(46, 204, 113)))  # Green
                amount_item.setForeground(QBrush(QColor(46, 204, 113)))
                amount_item.setFont(QFont("Verdana", 12, QFont.Bold))
            else:
                type_item.setForeground(QBrush(QColor(231, 76, 60)))   # Red
                amount_item.setForeground(QBrush(QColor(231, 76, 60)))
                amount_item.setFont(QFont("Verdana", 12, QFont.Bold))

    def go_back(self):
        from user_dashboard import UserDashboard
        self.dashboard = UserDashboard(self.account_no)
        self.dashboard.show()
        self.close()
