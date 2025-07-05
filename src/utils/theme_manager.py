"""
Theme Manager - Handle light/dark theme switching
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject

class ThemeManager(QObject):
    """Manages application themes"""
    
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        
    def apply_theme(self, theme_name):
        """Apply theme to application"""
        self.current_theme = theme_name
        
        if theme_name == "dark":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
            
    def apply_light_theme(self):
        """Apply light theme"""
        light_style = """
    QMainWindow {
        background-color: #ffffff;
        color: #2c3e50;
    }
    
    QWidget {
        background-color: #ffffff;
        color: #2c3e50;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    QFrame {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        color: #2c3e50;
    }
    
    QPushButton {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #0056b3;
    }
    
    QPushButton:pressed {
        background-color: #004085;
    }
    
    QPushButton:disabled {
        background-color: #6c757d;
        color: #ffffff;
    }
    
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
        background-color: white;
        border: 2px solid #ced4da;
        border-radius: 4px;
        padding: 6px;
        color: #2c3e50;
        font-size: 14px;
    }
    
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus {
        border-color: #007bff;
    }
    
    QLineEdit::placeholder {
        color: #6c757d;
    }
    
    QTableWidget {
        background-color: white;
        alternate-background-color: #f8f9fa;
        gridline-color: #dee2e6;
        color: #2c3e50;
    }
    
    QHeaderView::section {
        background-color: #e9ecef;
        color: #495057;
        padding: 8px;
        border: none;
        font-weight: bold;
    }
    
    QLabel {
        color: #2c3e50;
        background-color: transparent;
    }
    
    QGroupBox {
        font-weight: bold;
        border: 2px solid #dee2e6;
        border-radius: 5px;
        margin-top: 10px;
        color: #2c3e50;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
        color: #2c3e50;
    }
    
    QTabWidget::pane {
        border: 1px solid #dee2e6;
        background-color: white;
    }
    
    QTabBar::tab {
        background-color: #f8f9fa;
        color: #2c3e50;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: white;
        border-bottom: 2px solid #007bff;
    }
    
    QTabBar::tab:hover {
        background-color: #e9ecef;
    }
    
    QCheckBox {
        color: #2c3e50;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
    
    QCheckBox::indicator:unchecked {
        border: 2px solid #ced4da;
        background-color: white;
        border-radius: 3px;
    }
    
    QCheckBox::indicator:checked {
        border: 2px solid #007bff;
        background-color: #007bff;
        border-radius: 3px;
    }
    """
        
        QApplication.instance().setStyleSheet(light_style)
        
    def apply_dark_theme(self):
        """Apply dark theme"""
        dark_style = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QFrame {
            background-color: #3c3c3c;
            border: 1px solid #555555;
        }
        
        QPushButton {
            background-color: #0d7377;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        QPushButton:hover {
            background-color: #14a085;
        }
        
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
            background-color: #404040;
            border: 2px solid #555555;
            border-radius: 4px;
            padding: 6px;
            color: white;
        }
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
            border-color: #0d7377;
        }
        
        QTableWidget {
            background-color: #404040;
            alternate-background-color: #4a4a4a;
            gridline-color: #555555;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #505050;
            color: #ffffff;
            padding: 8px;
            border: none;
        }
        
        QLabel {
            color: #ffffff;
        }
        """
        
        QApplication.instance().setStyleSheet(dark_style)
