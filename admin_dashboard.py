#admin_dashboard
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                            QHBoxLayout, QMessageBox, QInputDialog, QLineEdit)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import bcrypt
import logging
from exception_handler import install_exception_handler

class AdminDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        install_exception_handler()
        self.admin_username = username
        self.setWindowTitle(f"Admin Dashboard - {username}")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
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
            .feature-box {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                min-width: 250px;
                border: 3px solid;
            }
            QLabel#feature-label {
                font-weight: bold;
                font-size: 16px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        # Logo
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(QPixmap("logo.png").scaled(120, 120, 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Admin Dashboard")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Feature Boxes Container
        features_container = QWidget()
        features_container.setStyleSheet("background: transparent;")
        features_layout = QHBoxLayout(features_container)
        features_layout.setSpacing(30)
        features_layout.setAlignment(Qt.AlignCenter)

        # Create colorful feature boxes
        users_box = self.create_feature_box("👥 View Users", "#3498db", self.view_all_users)
        trans_box = self.create_feature_box("💳 Transactions", "#2ecc71", self.view_transactions)
        search_box = self.create_feature_box("🔍 Search User", "#9b59b6", self.search_user)

        features_layout.addWidget(users_box)
        features_layout.addWidget(trans_box)
        features_layout.addWidget(search_box)

        # Logout Button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 16px;
                min-width: 200px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
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
        """Create a colorful feature box with icon"""
        box = QWidget()
        box.setObjectName("feature-box")
        box.setStyleSheet(f"border-color: {color};")

        layout = QVBoxLayout(box)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        
        # Add icon and text
        icon = QLabel(text.split()[0])
        icon.setStyleSheet("font-size: 24px;")
        
        label = QLabel(" ".join(text.split()[1:]))
        label.setObjectName("feature-label")
        label.setStyleSheet(f"color: {color};")
        
        layout.addWidget(icon, alignment=Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        
        
        box.mousePressEvent = lambda event: callback()
        
        return box

    def verify_password(self):
        """Verify admin password before sensitive actions"""
        password, ok = QInputDialog.getText(
            self, 
            'Admin Verification', 
            'Enter your password:', 
            QLineEdit.Password
        )
        
        if ok and password:
            try:
                from db_config import get_db_connection
                conn, cursor = get_db_connection()
                cursor.execute(
                    "SELECT password_hash FROM admins WHERE username = %s", 
                    (self.admin_username,)
                )
                result = cursor.fetchone()
                
                if result and bcrypt.checkpw(password.encode(), result[0].encode()):
                    return True
                QMessageBox.warning(self, "Error", "Incorrect password!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
            finally:
                if 'conn' in locals():
                    conn.close()
        return False

    def view_all_users(self):
        if self.verify_password():
            try:
                from admin_view_users import AdminViewUsersWindow
                self.users_window = AdminViewUsersWindow(self.admin_username)
                self.users_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open users: {str(e)}")

    def view_transactions(self):
        if self.verify_password():
            try:
                from admin_view_transactions import AdminViewTransactionsWindow
                self.trans_window = AdminViewTransactionsWindow(self.admin_username)
                self.trans_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open transactions: {str(e)}")

    def search_user(self):
        if self.verify_password():
            try:
                from admin_search_user import AdminSearchUserWindow
                self.search_window = AdminSearchUserWindow(self.admin_username)
                self.search_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open search: {str(e)}")

    def logout(self):
        from main import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
