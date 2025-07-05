"""
Settings Module - System configuration - UPDATED
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QFrame, QComboBox,
                              QSpinBox, QDoubleSpinBox, QGroupBox, QGridLayout,
                              QCheckBox, QTextEdit, QMessageBox, QTabWidget,
                              QFileDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class SettingsModule(QWidget):
    """System settings module"""
    
    settings_changed = Signal()
    
    def __init__(self, user, db_manager):
        super().__init__()
        self.user = user
        self.db_manager = db_manager
        self.setup_ui()
        self.setup_connections()
        self.load_settings()
        
    def setup_ui(self):
        """Setup settings interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("⚙️ System Settings")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Tab widget for different setting categories
        self.tab_widget = QTabWidget()
        
        # General Settings Tab
        general_tab = self.create_general_tab()
        self.tab_widget.addTab(general_tab, "General")
        
        # Company Settings Tab
        company_tab = self.create_company_tab()
        self.tab_widget.addTab(company_tab, "Company")
        
        # User Account Tab
        account_tab = self.create_account_tab()
        self.tab_widget.addTab(account_tab, "Account")
        
        # Backup Tab
        backup_tab = self.create_backup_tab()
        self.tab_widget.addTab(backup_tab, "Backup")
        
        # Save button
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        self.save_button = QPushButton("💾 Save Settings")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        self.reset_button = QPushButton("🔄 Reset to Defaults")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)
        
        # Add to main layout
        layout.addWidget(header_frame)
        layout.addWidget(self.tab_widget, 1)
        layout.addWidget(button_frame)
        
        self.setLayout(layout)
        
    def create_general_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Language and Theme
        ui_group = QGroupBox("User Interface")
        ui_layout = QGridLayout()
        
        # Language
        ui_layout.addWidget(QLabel("Language:"), 0, 0)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "العربية"])
        ui_layout.addWidget(self.language_combo, 0, 1)
        
        # Theme
        ui_layout.addWidget(QLabel("Theme:"), 1, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        ui_layout.addWidget(self.theme_combo, 1, 1)
        
        # Currency - ADDED DZD
        ui_layout.addWidget(QLabel("Currency:"), 2, 0)
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["DZD", "USD", "EUR", "GBP", "SAR", "AED"])
        ui_layout.addWidget(self.currency_combo, 2, 1)
        
        ui_group.setLayout(ui_layout)
        
        # Receipt Settings
        receipt_group = QGroupBox("Receipt Settings")
        receipt_layout = QGridLayout()
        
        # Receipt Printer
        receipt_layout.addWidget(QLabel("Receipt Printer:"), 0, 0)
        self.printer_combo = QComboBox()
        self.printer_combo.addItems(["Default Printer", "Thermal Printer", "PDF Export"])
        receipt_layout.addWidget(self.printer_combo, 0, 1)
        
        # Auto Print
        self.auto_print_checkbox = QCheckBox("Auto Print Receipt")
        receipt_layout.addWidget(self.auto_print_checkbox, 1, 0, 1, 2)
        
        # Receipt Footer
        receipt_layout.addWidget(QLabel("Receipt Footer:"), 2, 0)
        self.receipt_footer_input = QTextEdit()
        self.receipt_footer_input.setMaximumHeight(80)
        self.receipt_footer_input.setPlaceholderText("Thank you for your business!")
        receipt_layout.addWidget(self.receipt_footer_input, 2, 1)
        
        receipt_group.setLayout(receipt_layout)
        
        layout.addWidget(ui_group)
        layout.addWidget(receipt_group)
        layout.addStretch()
        
        return tab
        
    def create_company_tab(self):
        """Create company settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Company Information
        company_group = QGroupBox("Company Information")
        company_layout = QGridLayout()
        
        # Company Name
        company_layout.addWidget(QLabel("Company Name:"), 0, 0)
        self.company_name_input = QLineEdit()
        company_layout.addWidget(self.company_name_input, 0, 1)
        
        # Address
        company_layout.addWidget(QLabel("Address:"), 1, 0)
        self.company_address_input = QTextEdit()
        self.company_address_input.setMaximumHeight(80)
        company_layout.addWidget(self.company_address_input, 1, 1)
        
        # Phone
        company_layout.addWidget(QLabel("Phone:"), 2, 0)
        self.company_phone_input = QLineEdit()
        company_layout.addWidget(self.company_phone_input, 2, 1)
        
        # Email
        company_layout.addWidget(QLabel("Email:"), 3, 0)
        self.company_email_input = QLineEdit()
        company_layout.addWidget(self.company_email_input, 3, 1)
        
        # Website
        company_layout.addWidget(QLabel("Website:"), 4, 0)
        self.company_website_input = QLineEdit()
        company_layout.addWidget(self.company_website_input, 4, 1)
        
        # Tax ID
        company_layout.addWidget(QLabel("Tax ID:"), 5, 0)
        self.company_tax_id_input = QLineEdit()
        company_layout.addWidget(self.company_tax_id_input, 5, 1)
        
        company_group.setLayout(company_layout)
        
        # Logo Settings
        logo_group = QGroupBox("Company Logo")
        logo_layout = QVBoxLayout()
        
        self.logo_path_label = QLabel("No logo selected")
        self.logo_path_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 5px;
                padding: 20px;
                text-align: center;
                background-color: #f9f9f9;
            }
        """)
        
        logo_button_layout = QHBoxLayout()
        self.select_logo_button = QPushButton("Select Logo")
        self.remove_logo_button = QPushButton("Remove Logo")
        
        logo_button_layout.addWidget(self.select_logo_button)
        logo_button_layout.addWidget(self.remove_logo_button)
        logo_button_layout.addStretch()
        
        logo_layout.addWidget(self.logo_path_label)
        logo_layout.addLayout(logo_button_layout)
        logo_group.setLayout(logo_layout)
        
        layout.addWidget(company_group)
        layout.addWidget(logo_group)
        layout.addStretch()
        
        return tab
        
    def create_account_tab(self):
        """Create user account settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Account Information
        account_group = QGroupBox("Account Information")
        account_layout = QGridLayout()
        
        # Current Username (read-only)
        account_layout.addWidget(QLabel("Current Username:"), 0, 0)
        self.current_username_label = QLabel(self.user['username'])
        self.current_username_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        account_layout.addWidget(self.current_username_label, 0, 1)
        
        # New Username
        account_layout.addWidget(QLabel("New Username:"), 1, 0)
        self.new_username_input = QLineEdit()
        self.new_username_input.setPlaceholderText("Enter new username")
        account_layout.addWidget(self.new_username_input, 1, 1)
        
        # Full Name
        account_layout.addWidget(QLabel("Full Name:"), 2, 0)
        self.full_name_input = QLineEdit()
        self.full_name_input.setText(self.user['full_name'])
        account_layout.addWidget(self.full_name_input, 2, 1)
        
        account_group.setLayout(account_layout)
        
        # Password Change
        password_group = QGroupBox("Change Password")
        password_layout = QGridLayout()
        
        # Current Password
        password_layout.addWidget(QLabel("Current Password:"), 0, 0)
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setPlaceholderText("Enter current password")
        password_layout.addWidget(self.current_password_input, 0, 1)
        
        # New Password
        password_layout.addWidget(QLabel("New Password:"), 1, 0)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Enter new password")
        password_layout.addWidget(self.new_password_input, 1, 1)
        
        # Confirm Password
        password_layout.addWidget(QLabel("Confirm Password:"), 2, 0)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        password_layout.addWidget(self.confirm_password_input, 2, 1)
        
        # Change Password Button
        self.change_password_button = QPushButton("🔒 Change Password")
        self.change_password_button.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        password_layout.addWidget(self.change_password_button, 3, 0, 1, 2)
        
        password_group.setLayout(password_layout)
        
        layout.addWidget(account_group)
        layout.addWidget(password_group)
        layout.addStretch()
        
        return tab
        
    def create_backup_tab(self):
        """Create backup settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Backup Operations
        backup_group = QGroupBox("Backup Operations")
        backup_layout = QVBoxLayout()
        
        # Manual Backup
        manual_frame = QFrame()
        manual_layout = QHBoxLayout(manual_frame)
        
        manual_label = QLabel("Create manual backup of your data:")
        self.backup_now_button = QPushButton("🗄️ Backup Now")
        self.backup_now_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        manual_layout.addWidget(manual_label)
        manual_layout.addStretch()
        manual_layout.addWidget(self.backup_now_button)
        
        # Restore Backup
        restore_frame = QFrame()
        restore_layout = QHBoxLayout(restore_frame)
        
        restore_label = QLabel("Restore data from backup file:")
        self.restore_button = QPushButton("📥 Restore Backup")
        self.restore_button.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e8650e;
            }
        """)
        
        restore_layout.addWidget(restore_label)
        restore_layout.addStretch()
        restore_layout.addWidget(self.restore_button)
        
        backup_layout.addWidget(manual_frame)
        backup_layout.addWidget(restore_frame)
        backup_group.setLayout(backup_layout)
        
        # Backup History
        history_group = QGroupBox("Backup History")
        history_layout = QVBoxLayout()
        
        self.backup_history_text = QTextEdit()
        self.backup_history_text.setReadOnly(True)
        self.backup_history_text.setMaximumHeight(200)
        self.backup_history_text.setPlaceholderText("No backup history available")
        
        history_layout.addWidget(self.backup_history_text)
        history_group.setLayout(history_layout)
        
        layout.addWidget(backup_group)
        layout.addWidget(history_group)
        layout.addStretch()
        
        return tab
        
    def setup_connections(self):
        """Setup signal connections"""
        self.save_button.clicked.connect(self.save_settings)
        self.reset_button.clicked.connect(self.reset_settings)
        self.select_logo_button.clicked.connect(self.select_logo)
        self.remove_logo_button.clicked.connect(self.remove_logo)
        self.backup_now_button.clicked.connect(self.backup_now)
        self.restore_button.clicked.connect(self.restore_backup)
        self.change_password_button.clicked.connect(self.change_password)
        
    def load_settings(self):
        """Load current settings from database"""
        # Load language
        language = self.db_manager.get_setting("language") or "en"
        if language == "ar":
            self.language_combo.setCurrentText("العربية")
        else:
            self.language_combo.setCurrentText("English")
            
        # Load theme
        theme = self.db_manager.get_setting("theme") or "light"
        self.theme_combo.setCurrentText(theme.title())
        
        # Load currency
        currency = self.db_manager.get_setting("currency") or "DZD"
        self.currency_combo.setCurrentText(currency)
        
        # Load company information
        self.company_name_input.setText(self.db_manager.get_setting("company_name") or "LKS POS System")
        self.company_address_input.setPlainText(self.db_manager.get_setting("company_address") or "")
        self.company_phone_input.setText(self.db_manager.get_setting("company_phone") or "")
        self.company_email_input.setText(self.db_manager.get_setting("company_email") or "")
        self.company_website_input.setText(self.db_manager.get_setting("company_website") or "")
        self.company_tax_id_input.setText(self.db_manager.get_setting("company_tax_id") or "")
        
        # Load receipt settings
        self.receipt_footer_input.setPlainText(self.db_manager.get_setting("receipt_footer") or "Thank you for your business!")
        
    def save_settings(self):
        """Save settings to database - FIXED"""
        try:
            print("Saving settings...")  # Debug print
            
            # Save language
            language = "ar" if self.language_combo.currentText() == "العربية" else "en"
            self.db_manager.update_setting("language", language)
            print(f"Saved language: {language}")
            
            # Save theme
            theme = self.theme_combo.currentText().lower()
            self.db_manager.update_setting("theme", theme)
            print(f"Saved theme: {theme}")
            
            # Save currency
            self.db_manager.update_setting("currency", self.currency_combo.currentText())
            print(f"Saved currency: {self.currency_combo.currentText()}")
            
            # Save company information
            self.db_manager.update_setting("company_name", self.company_name_input.text())
            self.db_manager.update_setting("company_address", self.company_address_input.toPlainText())
            self.db_manager.update_setting("company_phone", self.company_phone_input.text())
            self.db_manager.update_setting("company_email", self.company_email_input.text())
            self.db_manager.update_setting("company_website", self.company_website_input.text())
            self.db_manager.update_setting("company_tax_id", self.company_tax_id_input.text())
            
            # Save receipt settings
            self.db_manager.update_setting("receipt_footer", self.receipt_footer_input.toPlainText())
            
            # Update user account if changed
            new_username = self.new_username_input.text().strip()
            full_name = self.full_name_input.text().strip()
            
            if new_username and new_username != self.user['username']:
                self.update_username(new_username)
                
            if full_name and full_name != self.user['full_name']:
                self.update_full_name(full_name)
            
            # Log activity
            self.db_manager.log_activity(self.user['id'], "settings_updated", "System settings updated")
            
            QMessageBox.information(self, "Success", "Settings saved successfully!\nSome changes may require restart to take full effect.")
            
            # Emit signal to apply changes immediately
            print("Emitting settings_changed signal...")
            self.settings_changed.emit()
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
            
    def update_username(self, new_username):
        """Update username"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, self.user['id']))
            conn.commit()
            conn.close()
            
            self.user['username'] = new_username
            self.current_username_label.setText(new_username)
            self.new_username_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update username: {str(e)}")
            
    def update_full_name(self, full_name):
        """Update full name"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET full_name = ? WHERE id = ?", (full_name, self.user['id']))
            conn.commit()
            conn.close()
            
            self.user['full_name'] = full_name
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update full name: {str(e)}")
            
    def change_password(self):
        """Change user password"""
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not current_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Validation Error", "Please fill in all password fields.")
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "New passwords do not match.")
            return
            
        if len(new_password) < 6:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters long.")
            return
            
        # Verify current password
        if not self.db_manager.verify_password(current_password, self.user['password_hash']):
            QMessageBox.warning(self, "Validation Error", "Current password is incorrect.")
            return
            
        try:
            # Update password
            new_password_hash = self.db_manager.hash_password(new_password)
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_password_hash, self.user['id']))
            conn.commit()
            conn.close()
            
            # Clear password fields
            self.current_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
            
            QMessageBox.information(self, "Success", "Password changed successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to change password: {str(e)}")
            
    def reset_settings(self):
        """Reset settings to defaults"""
        reply = QMessageBox.question(self, "Reset Settings",
                                   "Are you sure you want to reset all settings to defaults?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Reset to default values
            self.language_combo.setCurrentText("English")
            self.theme_combo.setCurrentText("Light")
            self.currency_combo.setCurrentText("DZD")
            
            self.company_name_input.setText("LKS POS System")
            self.company_address_input.setPlainText("123 Main St, City, State")
            self.company_phone_input.setText("+213-XXX-XXX-XXX")
            self.company_email_input.clear()
            self.company_website_input.clear()
            self.company_tax_id_input.clear()
            
            self.receipt_footer_input.setPlainText("Thank you for your business!")
            
    def select_logo(self):
        """Select company logo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Company Logo", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.logo_path_label.setText(f"Logo: {file_path}")
            self.db_manager.update_setting("company_logo", file_path)
            
    def remove_logo(self):
        """Remove company logo"""
        self.logo_path_label.setText("No logo selected")
        self.db_manager.update_setting("company_logo", "")
        
    def backup_now(self):
        """Create manual backup"""
        try:
            from datetime import datetime
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Backup", 
                f"lks_pos_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                "Database Files (*.db)"
            )
            
            if file_path:
                import shutil
                shutil.copy2(self.db_manager.db_path, file_path)
                
                # Log backup
                self.db_manager.log_activity(self.user['id'], "backup_created", f"Manual backup created: {file_path}")
                
                QMessageBox.information(self, "Backup Complete", 
                                      f"Backup created successfully:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Backup Error", f"Failed to create backup: {str(e)}")
            
    def restore_backup(self):
        """Restore from backup"""
        reply = QMessageBox.warning(self, "Restore Backup",
                                  "Restoring from backup will replace all current data.\n"
                                  "Are you sure you want to continue?",
                                  QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Backup File", "",
                "Database Files (*.db)"
            )
            
            if file_path:
                try:
                    import shutil
                    shutil.copy2(file_path, self.db_manager.db_path)
                    
                    QMessageBox.information(self, "Restore Complete", 
                                          "Backup restored successfully!\n"
                                          "Please restart the application.")
                    
                except Exception as e:
                    QMessageBox.critical(self, "Restore Error", f"Failed to restore backup: {str(e)}")
