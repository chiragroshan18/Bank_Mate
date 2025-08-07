#admin_view_transactions
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, 
                            QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import Qt
from db_config import get_db_connection

class AdminViewTransactionsWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("View Transactions - Bank Mate")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF1D0;
                font-family: 'Arial';
            }
            .header {
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
                margin-bottom: 20px;
            }
            QTableWidget {
                background-color: white;
                border-radius: 10px;
                padding: 5px;
                border: 2px solid #ddd;
                alternate-background-color: #f9f9f9;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                font-size: 14px;
            }
            .action-btn {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            .action-btn:hover {
                background-color: #e67e22;
            }
            #footer {
                color: #7f8c8d;
                font-size: 11px;
                font-weight: bold;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 20)
        main_layout.setSpacing(20)

        # Logo and Header
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        title = QLabel("💳 All Transactions")
        title.setObjectName("header")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Transactions Table with unique design
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Account No", "Type", "Amount", "Timestamp"])
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        # Back Button
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setObjectName("action-btn")
        back_btn.clicked.connect(self.go_back)
        main_layout.addWidget(back_btn, alignment=Qt.AlignRight)

        # Footer
        footer = QLabel("© Chirag - Bank Mate 2025")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignRight)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)
        self.load_transactions()

    def load_transactions(self):
        conn, cursor = get_db_connection()
        if conn:
            try:
                cursor.execute("SELECT account_no, type, amount, timestamp FROM transactions ORDER BY timestamp DESC")
                records = cursor.fetchall()
                self.table.setRowCount(len(records))
                
                for row_idx, row_data in enumerate(records):
                    for col_idx, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data))
                        item.setTextAlignment(Qt.AlignCenter)
                        
                        
                        if col_idx == 1:  
                            if "deposit" in str(data).lower():
                                item.setForeground(QColor('#2ecc71'))  # Green for deposits
                            elif "withdraw" in str(data).lower():
                                item.setForeground(QColor('#e74c3c'))  # Red for withdrawals
                            elif "transfer" in str(data).lower():
                                item.setForeground(QColor('#3498db'))  # Blue for transfers
                        
                        
                        if col_idx == 2:  # Amount column
                            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        
                        self.table.setItem(row_idx, col_idx, item)
                
                self.table.resizeColumnsToContents()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load transactions: {e}")
            finally:
                cursor.close()
                conn.close()

    def go_back(self):
        from admin_dashboard import AdminDashboard
        self.dashboard = AdminDashboard(self.username)
        self.dashboard.show()
        self.close()
