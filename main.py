"""
LKS POS System - Single Window Application
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtGui import QIcon, QFont

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.database_manager import DatabaseManager
from src.ui.main_application import MainApplication

class POSApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_application()
        self.init_database()
        
    def setup_application(self):
        """Setup application properties"""
        self.app.setApplicationName("LKS POS System")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("LKS Solutions")
        
        # Set application font
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)
        
        # Set global stylesheet
        self.app.setStyleSheet("""
            * {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            QWidget {
                background-color: #ffffff;
                color: #2c3e50;
            }
        """)
        
    def init_database(self):
        """Initialize database"""
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
        self.db_manager.create_default_admin()
        
    def run(self):
        """Run the application"""
        # Show main application window
        self.main_app = MainApplication()
        self.main_app.show()
        
        return self.app.exec()

if __name__ == "__main__":
    app = POSApplication()
    sys.exit(app.run())
