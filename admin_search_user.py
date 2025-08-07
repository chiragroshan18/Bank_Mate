#admin_search_user
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, 
                            QHeaderView, QFrame)
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtCore import Qt
from db_config import get_db_connection

class AdminSearchUserWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Search User - Bank Mate")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF1D0;
                font-family: 'Arial';
            }
            .header {
                font-size: 28px;
                font-weight: bold;
                color: #2C3E50;
                margin-bottom: 20px;
            }
            .search-box {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                border: 2px solid #ddd;
            }
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QTableWidget {
                background-color: white;
                border-radius: 10px;
                padding: 5px;
                border: 2px solid #ddd;
                alternate-background-color: #f9f9f9;
                gridline-color: #e0e0e0;
                font-size: 18px;
            }
            QTableWidget::item {
                padding: 20px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 20px;
                font-weight: bold;
                border: none;
                font-size: 18px;
            }
            .action-btn {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            .action-btn:hover {
                background-color: #e67e22;
            }
            #footer {
                color: #7f8c8d;
                font-size: 12px;
                font-weight: bold;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 30)
        main_layout.setSpacing(20)

        # Logo and Header
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(120, 120, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        title = QLabel("🔍 Search User")
        title.setObjectName("header")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Search Box
        search_frame = QFrame()
        search_frame.setObjectName("search-box")
        search_layout = QVBoxLayout(search_frame)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Account Number")
        search_layout.addWidget(self.search_input)

        search_btn = QPushButton("Search User")
        search_btn.setObjectName("action-btn")
        search_btn.setIcon(QIcon.fromTheme("system-search"))
        search_btn.clicked.connect(self.search_user)
        search_layout.addWidget(search_btn)

        main_layout.addWidget(search_frame)

        # Results Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Account No", "Name", "Balance"])
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Set larger font for the table
        font = QFont()
        font.setPointSize(16)  
        self.table.setFont(font)
        
        # Set row height
        self.table.verticalHeader().setDefaultSectionSize(60)  
        
        main_layout.addWidget(self.table)

        # Action Buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setObjectName("action-btn")
        back_btn.setIcon(QIcon.fromTheme("go-previous"))
        back_btn.clicked.connect(self.go_back)
        btn_layout.addWidget(back_btn, alignment=Qt.AlignRight)

        main_layout.addWidget(btn_frame)

        # Footer
        footer = QLabel("© Chirag - Bank Mate 2025")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignRight)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def search_user(self):
        account_no = self.search_input.text().strip()
        if not account_no.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid numeric account number.")
            return

        conn, cursor = get_db_connection()
        if conn:
            try:
                cursor.execute("SELECT account_no, name, balance FROM users WHERE account_no = %s", (account_no,))
                record = cursor.fetchone()
                
                if record:
                    self.table.setRowCount(1)
                    for col_idx, data in enumerate(record):
                        item = QTableWidgetItem(str(data))
                        item.setTextAlignment(Qt.AlignCenter)
                        
                        # Set comfortable font size for items
                        font = QFont()
                        font.setPointSize(16)
                        item.setFont(font)
                        
                        # Highlight balance column
                        if col_idx == 2:  
                            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                            try:
                                balance = float(data)
                                if balance < 0:
                                    item.setForeground(QColor('#e74c3c'))  # Red for negative
                                elif balance > 10000:
                                    item.setForeground(QColor('#2ecc71'))  # Green for high balance
                            except ValueError:
                                pass
                        
                        self.table.setItem(0, col_idx, item)
                else:
                    QMessageBox.information(self, "Not Found", "No user found with that account number.")
                    self.table.setRowCount(0)
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def go_back(self):
        from admin_dashboard import AdminDashboard
        self.dashboard = AdminDashboard(self.username)
        self.dashboard.show()
        self.close()
