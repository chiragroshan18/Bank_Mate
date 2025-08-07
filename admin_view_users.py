# admin_view_users
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, 
                            QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from db_config import get_db_connection

class AdminViewUsersWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("View All Users - Bank Mate")
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
                padding: 10px;
                border: 2px solid #ddd;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            .action-box {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                border: 3px solid #f39c12;
            }
            .action-btn {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            .action-btn:hover {
                background-color: #e67e22;
            }
            .action-btn-icon {
                margin-right: 8px;
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

        title = QLabel("👤 All Users")
        title.setObjectName("header")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Users Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Account No", "Name", "Balance"])
        self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table)

        # Action Box
        action_box = QWidget()
        action_box.setObjectName("action-box")
        action_layout = QHBoxLayout(action_box)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("action-btn")
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.clicked.connect(self.load_users)
        
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setObjectName("action-btn")
        back_btn.setIcon(QIcon.fromTheme("go-previous"))
        back_btn.clicked.connect(self.go_back)
        
        action_layout.addWidget(refresh_btn)
        action_layout.addWidget(back_btn)
        main_layout.addWidget(action_box)

        # Footer
        footer = QLabel("© Chirag - Bank Mate 2025")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignRight)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)
        self.load_users()

    def load_users(self):
        conn, cursor = get_db_connection()
        if conn:
            try:
                cursor.execute("SELECT account_no, name, balance FROM users")
                records = cursor.fetchall()
                self.table.setRowCount(len(records))
                for row_idx, row_data in enumerate(records):
                    for col_idx, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(row_idx, col_idx, item)
                self.table.resizeColumnsToContents()
                QMessageBox.information(self, "Success", "User data refreshed successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Database Error: {e}")
            finally:
                cursor.close()
                conn.close()

    def go_back(self):
        from admin_dashboard import AdminDashboard
        self.dashboard = AdminDashboard(self.username)
        self.dashboard.show()
        self.close()
