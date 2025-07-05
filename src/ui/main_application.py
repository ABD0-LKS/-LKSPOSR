"""
Main Application - Single window with login and main interface - UPDATED
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QStackedWidget, QLabel, QPushButton, QFrame,
                              QLineEdit, QComboBox, QCheckBox, QMessageBox,
                              QSpacerItem, QSizePolicy, QScrollArea, QApplication)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QPixmap

from src.database.database_manager import DatabaseManager
from src.ui.modules.pos_module import POSModule
from src.ui.modules.inventory_module import InventoryModule
from src.ui.modules.reports_module import ReportsModule
from src.ui.modules.users_module import UsersModule
from src.ui.modules.settings_module import SettingsModule
from src.utils.theme_manager import ThemeManager

class LoginPage(QWidget):
    """Login page widget - UPDATED"""
    
    login_successful = Signal(dict)
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup login interface"""
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side - branding/image
        left_panel = QFrame()
        left_panel.setFixedWidth(500)
        left_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
            }
        """)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setSpacing(30)
        
        # Logo and branding - UPDATED NAME
        logo_label = QLabel("🏪")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 120px; color: white;")
        
        brand_title = QLabel("LKS POS System")  # CHANGED NAME
        brand_title.setAlignment(Qt.AlignCenter)
        brand_title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        brand_title.setStyleSheet("color: white; margin: 20px 0;")
        
        brand_subtitle = QLabel("Complete Point of Sale Solution")
        brand_subtitle.setAlignment(Qt.AlignCenter)
        brand_subtitle.setFont(QFont("Segoe UI", 16))
        brand_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        features_label = QLabel("✓ Inventory Management\n✓ Sales Reports\n✓ User Management\n✓ Multi-language Support")
        features_label.setAlignment(Qt.AlignCenter)
        features_label.setFont(QFont("Segoe UI", 14))
        features_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); line-height: 1.6;")
        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(brand_title)
        left_layout.addWidget(brand_subtitle)
        left_layout.addWidget(features_label)
        
        # Right side - login form
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #ffffff;")
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(80, 80, 80, 80)
        
        # Login form container
        form_container = QFrame()
        form_container.setMaximumWidth(400)
        form_container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 40px;
            }
        """)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)
        
        # Form title
        form_title = QLabel("Welcome Back")
        form_title.setAlignment(Qt.AlignCenter)
        form_title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        form_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        
        form_subtitle = QLabel("Sign in to your account")
        form_subtitle.setAlignment(Qt.AlignCenter)
        form_subtitle.setFont(QFont("Segoe UI", 14))
        form_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        
        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        username_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont("Segoe UI", 14))
        self.username_input.setMinimumHeight(50)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 20px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2c3e50;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
                background-color: #ffffff;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #95a5a6;
            }
        """)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        password_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 14))
        self.password_input.setMinimumHeight(50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 20px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2c3e50;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
                background-color: #ffffff;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #95a5a6;
            }
        """)
        
        # Remember me and language
        options_layout = QHBoxLayout()
        
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setFont(QFont("Segoe UI", 12))
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #7f8c8d;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #bdc3c7;
                background-color: #ffffff;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #667eea;
                background-color: #667eea;
                border-radius: 3px;
            }
        """)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "العربية"])
        self.language_combo.setFont(QFont("Segoe UI", 12))
        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                background-color: #f8f9fa;
                color: #2c3e50;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #667eea;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
            }
        """)
        
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        options_layout.addWidget(self.language_combo)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.login_button.setMinimumHeight(55)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 18px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6fd8, stop:1 #6a4190);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4e5bc6, stop:1 #5e377e);
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.status_label.setMinimumHeight(30)
        
        # Add widgets to form
        form_layout.addWidget(form_title)
        form_layout.addWidget(form_subtitle)
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addLayout(options_layout)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.status_label)
        
        right_layout.addWidget(form_container)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Set default values for testing
        self.username_input.setText("admin")
        self.password_input.setText("admin123")
        
    def setup_connections(self):
        """Setup signal connections"""
        self.login_button.clicked.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.password_input.setFocus)
        
    def handle_login(self):
        """Handle login attempt"""
        print("Login button clicked!")
        
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        print(f"Username: '{username}', Password: '{password}'")
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Show processing state
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")
        self.status_label.setText("Authenticating...")
        self.status_label.setStyleSheet("color: #3498db;")
        
        # Force GUI update
        QApplication.processEvents()
        
        try:
            # Authenticate user
            print("Attempting authentication...")
            user = self.db_manager.authenticate_user(username, password)
            print(f"Authentication result: {user}")
            
            if user:
                self.show_success("Login successful!")
                print("Emitting login_successful signal...")
                # Emit signal with user data
                QTimer.singleShot(500, lambda: self.login_successful.emit(user))
            else:
                self.show_error("Invalid username or password")
                self.reset_login_button()
                
        except Exception as e:
            print(f"Login error: {e}")
            self.show_error(f"Login error: {str(e)}")
            self.reset_login_button()
            
    def reset_login_button(self):
        """Reset login button state"""
        self.login_button.setEnabled(True)
        self.login_button.setText("Sign In")
            
    def show_error(self, message):
        """Show error message"""
        print(f"Showing error: {message}")
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                background-color: #fdf2f2;
                border: 1px solid #f5c6cb;
                padding: 10px;
                border-radius: 6px;
                margin: 5px 0;
            }
        """)
        
    def show_success(self, message):
        """Show success message"""
        print(f"Showing success: {message}")
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #27ae60;
                background-color: #f0f9f0;
                border: 1px solid #c3e6cb;
                padding: 10px;
                border-radius: 6px;
                margin: 5px 0;
            }
        """)

class SidebarButton(QPushButton):
    """Custom sidebar button"""
    
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"{icon_text}  {text}")
        self.setCheckable(True)
        self.setMinimumHeight(55)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 18px 25px;
                border: none;
                background-color: transparent;
                color: #2c3e50;
                font-size: 15px;
                font-weight: 500;
                border-radius: 8px;
                margin: 2px 8px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                color: #667eea;
            }
            QPushButton:checked {
                background-color: #667eea;
                color: white;
                font-weight: bold;
            }
        """)

class MainDashboard(QWidget):
    """Main dashboard with sidebar and content area"""
    
    logout_requested = Signal()  # NEW SIGNAL
    
    def __init__(self, user, db_manager):
        super().__init__()
        self.user = user
        self.db_manager = db_manager
        self.theme_manager = ThemeManager()  # ADD THEME MANAGER
        self.current_module = None
        self.setup_ui()
        self.setup_connections()
        self.load_module("pos")
        
    def setup_ui(self):
        """Setup main dashboard interface"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content area
        self.create_content_area()
        
        # Add to main layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_area, 1)
        
        self.setLayout(main_layout)
        
    def create_sidebar(self):
        """Create sidebar navigation"""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(280)
        self.sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-right: 1px solid #e1e8ed;
            }
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Header
        header_frame = QFrame()
        header_frame.setMinimumHeight(100)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-bottom: 1px solid #e1e8ed;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 20, 25, 20)
        header_layout.setSpacing(5)
        
        # Logo and title - UPDATED NAME
        logo_label = QLabel("🏪 LKS POS System")  # CHANGED NAME
        logo_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        logo_label.setStyleSheet("color: white;")
        
        # User info
        user_label = QLabel(f"Welcome, {self.user['full_name']}")
        user_label.setFont(QFont("Segoe UI", 12))
        user_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        role_label = QLabel(f"Role: {self.user['role'].title()}")
        role_label.setFont(QFont("Segoe UI", 10))
        role_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(user_label)
        header_layout.addWidget(role_label)
        
        # Navigation
        nav_frame = QFrame()
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 20, 0, 0)
        nav_layout.setSpacing(5)
        
        # Navigation title
        nav_title = QLabel("NAVIGATION")
        nav_title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        nav_title.setStyleSheet("color: #7f8c8d; padding: 10px 25px; margin-bottom: 10px;")
        nav_layout.addWidget(nav_title)
        
        # Create navigation buttons
        self.nav_buttons = {}
        
        # POS - Available to all roles
        self.nav_buttons['pos'] = SidebarButton("Point of Sale", "🛒")
        nav_layout.addWidget(self.nav_buttons['pos'])
        
        # Inventory - Available to admin and stock_manager
        if self.user['role'] in ['admin', 'stock_manager']:
            self.nav_buttons['inventory'] = SidebarButton("Inventory", "📦")
            nav_layout.addWidget(self.nav_buttons['inventory'])
        
        # Reports - Available to admin and cashier
        if self.user['role'] in ['admin', 'cashier']:
            self.nav_buttons['reports'] = SidebarButton("Reports", "📊")
            nav_layout.addWidget(self.nav_buttons['reports'])
        
        # Users - Admin only
        if self.user['role'] == 'admin':
            self.nav_buttons['users'] = SidebarButton("User Management", "👥")
            nav_layout.addWidget(self.nav_buttons['users'])
        
        # Settings - Available to all
        self.nav_buttons['settings'] = SidebarButton("Settings", "⚙️")
        nav_layout.addWidget(self.nav_buttons['settings'])
        
        nav_layout.addStretch()
        
        # Logout button
        logout_frame = QFrame()
        logout_layout = QVBoxLayout(logout_frame)
        logout_layout.setContentsMargins(15, 15, 15, 25)
        
        self.logout_button = QPushButton("🚪  Logout")
        self.logout_button.setMinimumHeight(45)
        self.logout_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        logout_layout.addWidget(self.logout_button)
        
        # Add to sidebar
        sidebar_layout.addWidget(header_frame)
        sidebar_layout.addWidget(nav_frame, 1)
        sidebar_layout.addWidget(logout_frame)
        
    def create_content_area(self):
        """Create content area for modules"""
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("""
            QStackedWidget {
                background-color: #f8f9fa;
                border: none;
            }
        """)
        
        # Initialize modules
        self.modules = {}
        
        # Create a simple welcome page first
        welcome_page = QWidget()
        welcome_layout = QVBoxLayout(welcome_page)
        welcome_layout.setAlignment(Qt.AlignCenter)
        
        welcome_title = QLabel("🎉 Welcome to LKS POS System!")  # CHANGED NAME
        welcome_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        welcome_title.setAlignment(Qt.AlignCenter)
        welcome_title.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        welcome_text = QLabel("Select a module from the sidebar to get started")
        welcome_text.setFont(QFont("Segoe UI", 16))
        welcome_text.setAlignment(Qt.AlignCenter)
        welcome_text.setStyleSheet("color: #7f8c8d; margin: 10px;")
        
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_text)
        
        self.modules['welcome'] = welcome_page
        self.content_area.addWidget(welcome_page)
        
        # POS Module
        try:
            self.modules['pos'] = POSModule(self.user, self.db_manager)
            self.content_area.addWidget(self.modules['pos'])
        except Exception as e:
            print(f"Error loading POS module: {e}")
        
        # Inventory Module
        if self.user['role'] in ['admin', 'stock_manager']:
            try:
                self.modules['inventory'] = InventoryModule(self.user, self.db_manager)
                self.content_area.addWidget(self.modules['inventory'])
            except Exception as e:
                print(f"Error loading Inventory module: {e}")
        
        # Reports Module
        if self.user['role'] in ['admin', 'cashier']:
            try:
                self.modules['reports'] = ReportsModule(self.user, self.db_manager)
                self.content_area.addWidget(self.modules['reports'])
            except Exception as e:
                print(f"Error loading Reports module: {e}")
        
        # Users Module
        if self.user['role'] == 'admin':
            try:
                self.modules['users'] = UsersModule(self.user, self.db_manager)
                self.content_area.addWidget(self.modules['users'])
            except Exception as e:
                print(f"Error loading Users module: {e}")
        
        # Settings Module
        try:
            self.modules['settings'] = SettingsModule(self.user, self.db_manager)
            # Connect settings changed signal to apply changes
            self.modules['settings'].settings_changed.connect(self.apply_settings_changes)
            self.content_area.addWidget(self.modules['settings'])
        except Exception as e:
            print(f"Error loading Settings module: {e}")
        
    def setup_connections(self):
        """Setup signal connections"""
        # Navigation buttons
        for module_name, button in self.nav_buttons.items():
            button.clicked.connect(lambda checked, name=module_name: self.load_module(name))
        
        # Logout button - FIXED
        self.logout_button.clicked.connect(self.handle_logout)
        
    def load_module(self, module_name):
        """Load a specific module"""
        print(f"Loading module: {module_name}")
        
        if module_name in self.modules:
            # Update button states
            for name, button in self.nav_buttons.items():
                button.setChecked(name == module_name)
            
            # Switch to module
            self.content_area.setCurrentWidget(self.modules[module_name])
            self.current_module = module_name
            print(f"Switched to module: {module_name}")
        else:
            print(f"Module {module_name} not found!")
            
    def handle_logout(self):
        """Handle logout - FIXED"""
        print("Logout button clicked!")  # Debug print
        
        reply = QMessageBox.question(self, "Logout", 
                                   "Are you sure you want to logout?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            print("User confirmed logout")  # Debug print
            # Log activity
            try:
                self.db_manager.log_activity(self.user['id'], "logout", 
                                           f"User {self.user['username']} logged out")
            except Exception as e:
                print(f"Error logging activity: {e}")
            
            # Emit logout signal
            self.logout_requested.emit()
            
    def apply_settings_changes(self):
        """Apply settings changes immediately"""
        print("Applying settings changes...")
        
        # Apply theme changes
        theme = self.db_manager.get_setting("theme") or "light"
        self.theme_manager.apply_theme(theme)
        
        # Apply language changes (if needed)
        language = self.db_manager.get_setting("language") or "en"
        # Language changes would require app restart for full effect
        
        print(f"Applied theme: {theme}, language: {language}")

class MainApplication(QMainWindow):
    """Main application window - UPDATED"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup main application interface"""
        self.setWindowTitle("LKS POS System")  # CHANGED NAME
        self.setMinimumSize(1200, 800)
        self.showMaximized()
        
        # Central widget with stacked layout
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create login page
        self.login_page = LoginPage(self.db_manager)
        self.login_page.login_successful.connect(self.on_login_success)
        self.central_widget.addWidget(self.login_page)
        
        # Show login page initially
        self.central_widget.setCurrentWidget(self.login_page)
        
        print("Main application setup complete")
        
    def on_login_success(self, user):
        """Handle successful login"""
        print(f"Login successful for user: {user}")
        
        self.current_user = user
        
        try:
            # Create and show main dashboard
            print("Creating dashboard...")
            self.dashboard = MainDashboard(user, self.db_manager)
            # Connect logout signal - FIXED
            self.dashboard.logout_requested.connect(self.show_login)
            self.central_widget.addWidget(self.dashboard)
            self.central_widget.setCurrentWidget(self.dashboard)
            
            # Update window title
            self.setWindowTitle(f"LKS POS System - {user['full_name']} ({user['role'].title()})")  # CHANGED NAME
            
            print("Dashboard created and shown successfully!")
            
        except Exception as e:
            print(f"Error creating dashboard: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load dashboard: {str(e)}")
        
    def show_login(self):
        """Show login page (for logout) - FIXED"""
        print("Showing login page...")
        
        # Remove dashboard if it exists
        if hasattr(self, 'dashboard'):
            self.central_widget.removeWidget(self.dashboard)
            self.dashboard.deleteLater()
            del self.dashboard
            
        # Reset login form
        self.login_page.username_input.clear()
        self.login_page.password_input.clear()
        self.login_page.status_label.clear()
        self.login_page.login_button.setEnabled(True)
        self.login_page.login_button.setText("Sign In")
        
        # Show login page
        self.central_widget.setCurrentWidget(self.login_page)
        self.setWindowTitle("LKS POS System")  # CHANGED NAME
        self.current_user = None
        
        print("Login page shown successfully!")
