"""
Login Window - User authentication interface
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QFrame, QMessageBox,
                              QComboBox, QCheckBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QFont, QIcon

from src.database.database_manager import DatabaseManager
from src.ui.main_window import MainWindow
from src.utils.language_manager import LanguageManager

class LoginWindow(QWidget):
    login_successful = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.language_manager = LanguageManager()
        self.main_window = None
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the login interface"""
        self.setWindowTitle("POS System - Login")
        self.setFixedSize(500, 700)  # Made larger
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Set window background
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        
        # Center the window
        self.center_window()
        
        # Main layout with more spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Add top spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Logo/Title section
        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: transparent;")
        title_layout = QVBoxLayout(title_frame)
        title_layout.setSpacing(15)
        
        # Logo placeholder - much larger
        logo_label = QLabel("🏪")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 72px; margin-bottom: 20px; color: #1a73e8;")
        
        # Title - larger and bolder
        title_label = QLabel("POS System")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setStyleSheet("color: #1a73e8; margin-bottom: 10px;")
        
        # Subtitle
        subtitle_label = QLabel("Point of Sale Management System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #5f6368; font-size: 16px; margin-bottom: 20px;")
        
        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        # Login form with much better spacing
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(25)  # Much more spacing between elements
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet("""
            font-weight: bold; 
            color: #202124; 
            font-size: 16px;
            margin-bottom: 8px;
        """)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(50)  # Much taller
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 20px;
                border: 2px solid #dadce0;
                border-radius: 8px;
                font-size: 16px;
                background-color: white;
                color: #202124;
            }
            QLineEdit:focus {
                border-color: #1a73e8;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #9aa0a6;
            }
        """)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            font-weight: bold; 
            color: #202124; 
            font-size: 16px;
            margin-bottom: 8px;
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(50)  # Much taller
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 20px;
                border: 2px solid #dadce0;
                border-radius: 8px;
                font-size: 16px;
                background-color: white;
                color: #202124;
            }
            QLineEdit:focus {
                border-color: #1a73e8;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #9aa0a6;
            }
        """)
        
        # Language selection
        language_label = QLabel("Language")
        language_label.setStyleSheet("""
            font-weight: bold; 
            color: #202124; 
            font-size: 16px;
            margin-bottom: 8px;
        """)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "العربية"])
        self.language_combo.setMinimumHeight(50)  # Much taller
        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 15px 20px;
                border: 2px solid #dadce0;
                border-radius: 8px;
                font-size: 16px;
                background-color: white;
                color: #202124;
            }
            QComboBox:focus {
                border-color: #1a73e8;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #5f6368;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #dadce0;
                background-color: white;
                color: #202124;
                selection-background-color: #e8f0fe;
            }
        """)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #5f6368;
                font-size: 16px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #dadce0;
                background-color: white;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #1a73e8;
                background-color: #1a73e8;
                border-radius: 4px;
                image: none;
            }
            QCheckBox::indicator:checked:after {
                content: "✓";
                color: white;
                font-weight: bold;
            }
        """)
        
        # Login button - much larger and more prominent
        self.login_button = QPushButton("Sign In")
        self.login_button.setMinimumHeight(55)  # Much taller
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                padding: 18px 24px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #1246a0;
            }
            QPushButton:disabled {
                background-color: #dadce0;
                color: #9aa0a6;
            }
        """)
        
        # Add widgets to form with proper spacing
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(language_label)
        form_layout.addWidget(self.language_combo)
        form_layout.addWidget(self.remember_checkbox)
        form_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        form_layout.addWidget(self.login_button)
        
        # Status label with better styling
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setMinimumHeight(40)
        self.status_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                margin: 10px 0;
            }
        """)
        
        # Add to main layout
        main_layout.addWidget(title_frame)
        main_layout.addWidget(form_frame)
        main_layout.addWidget(self.status_label)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(main_layout)
        
        # Set default values for testing
        self.username_input.setText("admin")
        self.password_input.setText("admin123")
        
    def setup_connections(self):
        """Setup signal connections"""
        self.login_button.clicked.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.password_input.setFocus)
        self.language_combo.currentTextChanged.connect(self.change_language)
        
    def center_window(self):
        """Center the window on screen"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def handle_login(self):
        """Handle login attempt"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Disable login button during authentication
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")
        
        # Authenticate user
        user = self.db_manager.authenticate_user(username, password)
        
        if user:
            self.show_success("Login successful!")
            
            # Open main window after short delay
            QTimer.singleShot(1000, lambda: self.open_main_window(user))
        else:
            self.show_error("Invalid username or password")
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In")
            
    def show_error(self, message):
        """Show error message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #d93025;
                font-weight: bold;
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                margin: 10px 0;
            }
        """)
        
    def show_success(self, message):
        """Show success message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #137333;
                font-weight: bold;
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                margin: 10px 0;
            }
        """)
        
    def change_language(self, language):
        """Change application language"""
        if language == "العربية":
            self.language_manager.set_language("ar")
        else:
            self.language_manager.set_language("en")
            
    def open_main_window(self, user):
        """Open main application window"""
        self.main_window = MainWindow(user)
        self.main_window.show()
        self.close()
