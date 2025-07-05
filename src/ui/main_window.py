"""
Main Window - Primary application interface with improved design
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                              QStackedWidget, QLabel, QPushButton, QFrame,
                              QScrollArea, QMessageBox, QMenuBar, QStatusBar,
                              QToolBar, QSizePolicy, QSpacerItem)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QIcon, QFont, QAction

from src.ui.modules.pos_module import POSModule
from src.ui.modules.inventory_module import InventoryModule
from src.ui.modules.reports_module import ReportsModule
from src.ui.modules.users_module import UsersModule
from src.ui.modules.settings_module import SettingsModule
from src.utils.theme_manager import ThemeManager
from src.database.database_manager import DatabaseManager

class SidebarButton(QPushButton):
    """Custom sidebar button with better styling"""
    
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"{icon_text}  {text}")
        self.setCheckable(True)
        self.setMinimumHeight(60)  # Much taller buttons
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 20px 25px;
                border: none;
                background-color: transparent;
                color: #202124;
                font-size: 16px;
                font-weight: 500;
                border-radius: 8px;
                margin: 2px 10px;
            }
            QPushButton:hover {
                background-color: #f1f3f4;
                color: #1a73e8;
            }
            QPushButton:checked {
                background-color: #e8f0fe;
                color: #1a73e8;
                font-weight: bold;
                border-left: 4px solid #1a73e8;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db_manager = DatabaseManager()
        self.theme_manager = ThemeManager()
        self.current_module = None
        
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_connections()
        
        # Load default module
        self.load_module("pos")
        
    def setup_ui(self):
        """Setup the main user interface with better spacing"""
        self.setWindowTitle(f"POS System - Welcome {self.user['full_name']}")
        self.setMinimumSize(1400, 900)  # Larger minimum size
        self.showMaximized()
        
        # Set main window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
                color: #202124;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content area
        self.create_content_area()
        
        # Add to main layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_area, 1)
        
    def create_sidebar(self):
        """Create the sidebar navigation with better design"""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(300)  # Wider sidebar
        self.sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: #fafbfc;
                border-right: 1px solid #dadce0;
            }
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Header with better styling
        header_frame = QFrame()
        header_frame.setMinimumHeight(120)  # Taller header
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1a73e8;
                color: white;
                border-bottom: 1px solid #1557b0;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 25, 25, 25)
        header_layout.setSpacing(8)
        
        # Logo and title
        logo_label = QLabel("🏪 POS System")
        logo_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        
        # User info
        user_label = QLabel(f"Welcome, {self.user['full_name']}")
        user_label.setStyleSheet("font-size: 14px; color: #e8f0fe; margin-top: 5px;")
        
        role_label = QLabel(f"Role: {self.user['role'].title()}")
        role_label.setStyleSheet("font-size: 12px; color: #aecbfa;")
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(user_label)
        header_layout.addWidget(role_label)
        
        # Navigation section
        nav_frame = QFrame()
        nav_frame.setStyleSheet("background-color: #fafbfc;")
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 20, 0, 0)
        nav_layout.setSpacing(5)
        
        # Navigation title
        nav_title = QLabel("NAVIGATION")
        nav_title.setStyleSheet("""
            color: #5f6368;
            font-size: 12px;
            font-weight: bold;
            padding: 10px 25px;
            margin-bottom: 10px;
        """)
        nav_layout.addWidget(nav_title)
        
        # Create navigation buttons based on user role
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
        
        # Logout button with better styling
        logout_frame = QFrame()
        logout_layout = QVBoxLayout(logout_frame)
        logout_layout.setContentsMargins(15, 15, 15, 25)
        
        self.logout_button = QPushButton("🚪  Logout")
        self.logout_button.setMinimumHeight(50)
        self.logout_button.setStyleSheet("""
            QPushButton {
                text-align: center;
                padding: 15px 25px;
                border: 2px solid #ea4335;
                background-color: transparent;
                color: #ea4335;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ea4335;
                color: white;
            }
            QPushButton:pressed {
                background-color: #d33b2c;
            }
        """)
        
        logout_layout.addWidget(self.logout_button)
        
        # Add to sidebar
        sidebar_layout.addWidget(header_frame)
        sidebar_layout.addWidget(nav_frame, 1)
        sidebar_layout.addWidget(logout_frame)
        
    def create_content_area(self):
        """Create the main content area"""
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("""
            QStackedWidget {
                background-color: #ffffff;
                border: none;
            }
        """)
        
        # Initialize modules
        self.modules = {}
        
        # POS Module
        self.modules['pos'] = POSModule(self.user, self.db_manager)
        self.content_area.addWidget(self.modules['pos'])
        
        # Inventory Module
        if self.user['role'] in ['admin', 'stock_manager']:
            self.modules['inventory'] = InventoryModule(self.user, self.db_manager)
            self.content_area.addWidget(self.modules['inventory'])
        
        # Reports Module
        if self.user['role'] in ['admin', 'cashier']:
            self.modules['reports'] = ReportsModule(self.user, self.db_manager)
            self.content_area.addWidget(self.modules['reports'])
        
        # Users Module
        if self.user['role'] == 'admin':
            self.modules['users'] = UsersModule(self.user, self.db_manager)
            self.content_area.addWidget(self.modules['users'])
        
        # Settings Module
        self.modules['settings'] = SettingsModule(self.user, self.db_manager)
        self.content_area.addWidget(self.modules['settings'])
        
    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
                color: #202124;
                border-bottom: 1px solid #dadce0;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 8px 12px;
                margin: 2px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #f1f3f4;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_sale_action = QAction("New Sale", self)
        new_sale_action.setShortcut("Ctrl+N")
        new_sale_action.triggered.connect(lambda: self.load_module("pos"))
        file_menu.addAction(new_sale_action)
        
        file_menu.addSeparator()
        
        logout_action = QAction("Logout", self)
        logout_action.setShortcut("Ctrl+L")
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        toggle_theme_action = QAction("Toggle Theme", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                color: #5f6368;
                border-top: 1px solid #dadce0;
                padding: 5px;
            }
        """)
        
        # Current user label
        user_label = QLabel(f"Logged in as: {self.user['full_name']} ({self.user['role'].title()})")
        user_label.setStyleSheet("color: #5f6368; font-size: 14px;")
        self.status_bar.addPermanentWidget(user_label)
        
        # Current time
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #5f6368; font-size: 14px;")
        self.status_bar.addPermanentWidget(self.time_label)
        
        # Update time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        
    def setup_connections(self):
        """Setup signal connections"""
        # Navigation buttons
        for module_name, button in self.nav_buttons.items():
            button.clicked.connect(lambda checked, name=module_name: self.load_module(name))
        
        # Logout button
        self.logout_button.clicked.connect(self.logout)
        
    def load_module(self, module_name):
        """Load a specific module"""
        if module_name in self.modules:
            # Update button states
            for name, button in self.nav_buttons.items():
                button.setChecked(name == module_name)
            
            # Switch to module
            self.content_area.setCurrentWidget(self.modules[module_name])
            self.current_module = module_name
            
            # Update status bar
            module_titles = {
                'pos': 'Point of Sale',
                'inventory': 'Inventory Management',
                'reports': 'Reports & Analytics',
                'users': 'User Management',
                'settings': 'System Settings'
            }
            
            self.status_bar.showMessage(f"Current Module: {module_titles.get(module_name, module_name.title())}")
            
    def update_time(self):
        """Update the time display"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)
        
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current_theme = self.db_manager.get_setting("theme") or "light"
        new_theme = "dark" if current_theme == "light" else "light"
        
        self.theme_manager.apply_theme(new_theme)
        self.db_manager.update_setting("theme", new_theme)
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About POS System", 
                         "Modern POS System v1.0\n\n"
                         "A comprehensive Point of Sale solution\n"
                         "built with Python and PySide6.\n\n"
                         "Features:\n"
                         "• Point of Sale\n"
                         "• Inventory Management\n"
                         "• Sales Reports\n"
                         "• User Management\n"
                         "• Multi-language Support")
        
    def logout(self):
        """Logout and return to login screen"""
        reply = QMessageBox.question(self, "Logout", 
                                   "Are you sure you want to logout?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Log activity
            self.db_manager.log_activity(self.user['id'], "logout", 
                                       f"User {self.user['username']} logged out")
            
            # Close main window and show login
            from src.ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
            
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(self, "Exit", 
                                   "Are you sure you want to exit?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Log activity
            self.db_manager.log_activity(self.user['id'], "logout", 
                                       f"User {self.user['username']} closed application")
            event.accept()
        else:
            event.ignore()
