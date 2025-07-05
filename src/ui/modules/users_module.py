"""
Users Module - User management (Admin only)
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                              QFrame, QComboBox, QMessageBox, QDialog,
                              QDialogButtonBox, QGroupBox, QGridLayout,
                              QCheckBox, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class UserDialog(QDialog):
    """Dialog for adding/editing users"""
    
    def __init__(self, db_manager, user=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user = user
        self.is_edit_mode = user is not None
        self.setup_ui()
        
        if self.is_edit_mode:
            self.load_user_data()
            
    def setup_ui(self):
        """Setup user dialog UI"""
        title = "Edit User" if self.is_edit_mode else "Add New User"
        self.setWindowTitle(title)
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout()
        
        # User information
        info_group = QGroupBox("User Information")
        info_layout = QGridLayout()
        
        # Username
        info_layout.addWidget(QLabel("Username:"), 0, 0)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        info_layout.addWidget(self.username_input, 0, 1)
        
        # Full name
        info_layout.addWidget(QLabel("Full Name:"), 1, 0)
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        info_layout.addWidget(self.fullname_input, 1, 1)
        
        # Email
        info_layout.addWidget(QLabel("Email:"), 2, 0)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        info_layout.addWidget(self.email_input, 2, 1)
        
        # Role
        info_layout.addWidget(QLabel("Role:"), 3, 0)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["cashier", "stock_manager", "admin"])
        info_layout.addWidget(self.role_combo, 3, 1)
        
        # Password (only for new users or if changing)
        info_layout.addWidget(QLabel("Password:"), 4, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        info_layout.addWidget(self.password_input, 4, 1)
        
        # Confirm password
        info_layout.addWidget(QLabel("Confirm Password:"), 5, 0)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm password")
        info_layout.addWidget(self.confirm_password_input, 5, 1)
        
        # Active status
        self.active_checkbox = QCheckBox("User is active")
        self.active_checkbox.setChecked(True)
        info_layout.addWidget(self.active_checkbox, 6, 0, 1, 2)
        
        info_group.setLayout(info_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_user)
        button_box.rejected.connect(self.reject)
        
        # Layout
        layout.addWidget(info_group)
        layout.addStretch()
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # If editing, make password optional
        if self.is_edit_mode:
            self.password_input.setPlaceholderText("Leave blank to keep current password")
            self.confirm_password_input.setPlaceholderText("Leave blank to keep current password")
            
    def load_user_data(self):
        """Load existing user data for editing"""
        if not self.user:
            return
            
        self.username_input.setText(self.user['username'])
        self.fullname_input.setText(self.user['full_name'])
        self.email_input.setText(self.user.get('email', ''))
        
        # Set role
        role_index = self.role_combo.findText(self.user['role'])
        if role_index >= 0:
            self.role_combo.setCurrentIndex(role_index)
            
        self.active_checkbox.setChecked(bool(self.user.get('is_active', True)))
        
    def save_user(self):
        """Save user to database"""
        # Validate input
        username = self.username_input.text().strip()
        fullname = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_combo.currentText()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        is_active = self.active_checkbox.isChecked()
        
        if not username:
            QMessageBox.warning(self, "Validation Error", "Username is required.")
            return
            
        if not fullname:
            QMessageBox.warning(self, "Validation Error", "Full name is required.")
            return
            
        # Password validation
        if not self.is_edit_mode:  # New user
            if not password:
                QMessageBox.warning(self, "Validation Error", "Password is required for new users.")
                return
        
        if password:  # If password is provided
            if len(password) < 6:
                QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters long.")
                return
                
            if password != confirm_password:
                QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
                return
        
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            if self.is_edit_mode:
                # Update existing user
                if password:
                    password_hash = self.db_manager.hash_password(password)
                    cursor.execute('''
                        UPDATE users 
                        SET username=?, full_name=?, email=?, role=?, password_hash=?, is_active=?
                        WHERE id=?
                    ''', (username, fullname, email, role, password_hash, is_active, self.user['id']))
                else:
                    cursor.execute('''
                        UPDATE users 
                        SET username=?, full_name=?, email=?, role=?, is_active=?
                        WHERE id=?
                    ''', (username, fullname, email, role, is_active, self.user['id']))
            else:
                # Insert new user
                password_hash = self.db_manager.hash_password(password)
                cursor.execute('''
                    INSERT INTO users (username, full_name, email, role, password_hash, is_active)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, fullname, email, role, password_hash, is_active))
            
            conn.commit()
            conn.close()
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save user: {str(e)}")

class UsersModule(QWidget):
    """User management module"""
    
    def __init__(self, user, db_manager):
        super().__init__()
        self.user = user
        self.db_manager = db_manager
        self.setup_ui()
        self.setup_connections()
        self.load_users()
        
    def setup_ui(self):
        """Setup users interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("👥 User Management")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        
        # Action buttons
        self.add_user_button = QPushButton("➕ Add User")
        self.add_user_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.add_user_button)
        
        # Search section
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        search_layout = QHBoxLayout(search_frame)
        
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by username or full name...")
        
        role_label = Q
