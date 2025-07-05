"""
Inventory Module - Product and stock management - UPDATED
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                              QFrame, QComboBox, QSpinBox, QDoubleSpinBox,
                              QMessageBox, QDialog, QDialogButtonBox, QTextEdit,
                              QGridLayout, QGroupBox, QFileDialog, QTabWidget,
                              QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
import os

class CategoryDialog(QDialog):
    """Dialog for adding/editing categories"""
    
    def __init__(self, db_manager, category=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.category = category
        self.is_edit_mode = category is not None
        self.setup_ui()
        
        if self.is_edit_mode:
            self.load_category_data()
            
    def setup_ui(self):
        """Setup category dialog UI"""
        title = "Edit Category" if self.is_edit_mode else "Add New Category"
        self.setWindowTitle(title)
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Category information
        info_group = QGroupBox("Category Information")
        info_layout = QGridLayout()
        
        # Name
        info_layout.addWidget(QLabel("Category Name:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter category name")
        info_layout.addWidget(self.name_input, 0, 1)
        
        # Description
        info_layout.addWidget(QLabel("Description:"), 1, 0)
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.description_input.setPlaceholderText("Enter category description")
        info_layout.addWidget(self.description_input, 1, 1)
        
        info_group.setLayout(info_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_category)
        button_box.rejected.connect(self.reject)
        
        # Layout
        layout.addWidget(info_group)
        layout.addStretch()
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def load_category_data(self):
        """Load existing category data for editing"""
        if not self.category:
            return
            
        self.name_input.setText(self.category['name'])
        self.description_input.setPlainText(self.category.get('description', ''))
        
    def save_category(self):
        """Save category to database"""
        # Validate input
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Category name is required.")
            return
            
        description = self.description_input.toPlainText().strip()
        
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            if self.is_edit_mode:
                # Update existing category
                cursor.execute('''
                    UPDATE categories 
                    SET name=?, description=?
                    WHERE id=?
                ''', (name, description, self.category['id']))
            else:
                # Insert new category
                cursor.execute('''
                    INSERT INTO categories (name, description)
                    VALUES (?, ?)
                ''', (name, description))
            
            conn.commit()
            conn.close()
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save category: {str(e)}")

class ProductDialog(QDialog):
    """Dialog for adding/editing products"""

    def __init__(self, db_manager, product=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.product = product
        self.is_edit_mode = product is not None
        self.setup_ui()
        
        if self.is_edit_mode:
            self.load_product_data()
            
    def setup_ui(self):
        """Setup product dialog UI"""
        title = "Edit Product" if self.is_edit_mode else "Add New Product"
        self.setWindowTitle(title)
        self.setFixedSize(500, 600)
        
        layout = QVBoxLayout()
        
        # Product information
        info_group = QGroupBox("Product Information")
        info_layout = QGridLayout()
        
        # Name
        info_layout.addWidget(QLabel("Product Name:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        info_layout.addWidget(self.name_input, 0, 1)
        
        # Barcode
        info_layout.addWidget(QLabel("Barcode:"), 1, 0)
        barcode_layout = QHBoxLayout()
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Enter or generate barcode")
        self.generate_barcode_button = QPushButton("Generate")
        self.generate_barcode_button.clicked.connect(self.generate_barcode)
        barcode_layout.addWidget(self.barcode_input)
        barcode_layout.addWidget(self.generate_barcode_button)
        info_layout.addLayout(barcode_layout, 1, 1)
        
        # Category
        info_layout.addWidget(QLabel("Category:"), 2, 0)
        self.category_combo = QComboBox()
        self.load_categories()
        info_layout.addWidget(self.category_combo, 2, 1)
        
        # Description
        info_layout.addWidget(QLabel("Description:"), 3, 0)
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        info_layout.addWidget(self.description_input, 3, 1)
        
        info_group.setLayout(info_layout)
        
        # Pricing and inventory
        pricing_group = QGroupBox("Pricing & Inventory")
        pricing_layout = QGridLayout()
        
        # Cost price
        pricing_layout.addWidget(QLabel("Cost Price:"), 0, 0)
        self.cost_price_input = QDoubleSpinBox()
        self.cost_price_input.setRange(0, 99999.99)
        self.cost_price_input.setDecimals(2)
        self.cost_price_input.setSuffix(" DZD")
        pricing_layout.addWidget(self.cost_price_input, 0, 1)
        
        # Selling price
        pricing_layout.addWidget(QLabel("Selling Price:"), 1, 0)
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 99999.99)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" DZD")
        pricing_layout.addWidget(self.price_input, 1, 1)
        
        # Current quantity
        pricing_layout.addWidget(QLabel("Current Quantity:"), 2, 0)
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 99999)
        pricing_layout.addWidget(self.quantity_input, 2, 1)
        
        # Minimum quantity
        pricing_layout.addWidget(QLabel("Minimum Quantity:"), 3, 0)
        self.min_quantity_input = QSpinBox()
        self.min_quantity_input.setRange(0, 999)
        self.min_quantity_input.setValue(5)
        pricing_layout.addWidget(self.min_quantity_input, 3, 1)
        
        pricing_group.setLayout(pricing_layout)
        
        # Image section
        image_group = QGroupBox("Product Image")
        image_layout = QVBoxLayout()
        
        self.image_label = QLabel("No image selected")
        self.image_label.setFixedSize(200, 150)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 5px;
                text-align: center;
                background-color: #f9f9f9;
            }
        """)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.select_image_button = QPushButton("Select Image")
        self.select_image_button.clicked.connect(self.select_image)
        
        image_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        image_layout.addWidget(self.select_image_button)
        image_group.setLayout(image_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_product)
        button_box.rejected.connect(self.reject)
        
        # Layout
        layout.addWidget(info_group)
        layout.addWidget(pricing_group)
        layout.addWidget(image_group)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def load_categories(self):
        """Load categories into combo box"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = cursor.fetchall()
        conn.close()
        
        self.category_combo.clear()
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])
            
    def generate_barcode(self):
        """Generate a random barcode"""
        import random
        barcode = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        self.barcode_input.setText(barcode)
        
    def select_image(self):
        """Select product image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Product Image", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            # Load and display image
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_path = file_path
            else:
                QMessageBox.warning(self, "Error", "Could not load the selected image.")
                
    def load_product_data(self):
        """Load existing product data for editing"""
        if not self.product:
            return
            
        self.name_input.setText(self.product['name'])
        self.barcode_input.setText(self.product.get('barcode', ''))
        self.description_input.setPlainText(self.product.get('description', ''))
        self.cost_price_input.setValue(self.product.get('cost_price', 0))
        self.price_input.setValue(self.product['price'])
        self.quantity_input.setValue(self.product['quantity'])
        self.min_quantity_input.setValue(self.product.get('min_quantity', 5))
        
        # Set category
        if self.product.get('category_id'):
            for i in range(self.category_combo.count()):
                if self.category_combo.itemData(i) == self.product['category_id']:
                    self.category_combo.setCurrentIndex(i)
                    break
                    
        # Load image if exists
        if self.product.get('image_path') and os.path.exists(self.product['image_path']):
            pixmap = QPixmap(self.product['image_path'])
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_path = self.product['image_path']
                
    def save_product(self):
        """Save product to database"""
        # Validate input
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Product name is required.")
            return
            
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Selling price must be greater than 0.")
            return
            
        # Prepare data
        product_data = {
            'name': self.name_input.text().strip(),
            'barcode': self.barcode_input.text().strip() or None,
            'category_id': self.category_combo.currentData(),
            'description': self.description_input.toPlainText().strip(),
            'cost_price': self.cost_price_input.value(),
            'price': self.price_input.value(),
            'quantity': self.quantity_input.value(),
            'min_quantity': self.min_quantity_input.value(),
            'image_path': getattr(self, 'image_path', None)
        }
        
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            if self.is_edit_mode:
                # Update existing product
                cursor.execute('''
                    UPDATE products 
                    SET name=?, barcode=?, category_id=?, description=?, cost_price=?,
                        price=?, quantity=?, min_quantity=?, image_path=?, updated_at=CURRENT_TIMESTAMP
                    WHERE id=?
                ''', (*product_data.values(), self.product['id']))
            else:
                # Insert new product
                cursor.execute('''
                    INSERT INTO products (name, barcode, category_id, description, cost_price,
                                        price, quantity, min_quantity, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', tuple(product_data.values()))
            
            conn.commit()
            conn.close()
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save product: {str(e)}")

class InventoryModule(QWidget):
    """Inventory management module"""

    def __init__(self, user, db_manager):
        super().__init__()
        self.user = user
        self.db_manager = db_manager
        self.setup_ui()
        self.setup_connections()
        self.load_products()
        
    def setup_ui(self):
        """Setup inventory interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("📦 Inventory Management")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        
        # Action buttons
        self.add_product_button = QPushButton("➕ Add Product")
        self.add_product_button.setStyleSheet("""
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
        
        self.add_category_button = QPushButton("📁 Add Category")
        self.add_category_button.setStyleSheet("""
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
        
        self.import_button = QPushButton("📥 Import")
        self.export_button = QPushButton("📤 Export")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.add_category_button)
        header_layout.addWidget(self.add_product_button)
        header_layout.addWidget(self.import_button)
        header_layout.addWidget(self.export_button)
        
        # Search and filter section
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or barcode...")
        
        # Category filter
        category_label = QLabel("Category:")
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories", None)
        self.load_category_filter()
        
        # Stock filter
        stock_label = QLabel("Stock Status:")
        self.stock_filter = QComboBox()
        self.stock_filter.addItems(["All Items", "In Stock", "Low Stock", "Out of Stock"])
        
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input, 1)
        filter_layout.addWidget(category_label)
        filter_layout.addWidget(self.category_filter)
        filter_layout.addWidget(stock_label)
        filter_layout.addWidget(self.stock_filter)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Name", "Barcode", "Category", "Price", "Cost", "Stock", "Min Stock", "Actions"
        ])
        
        # Table styling
        self.products_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        # Configure table
        self.products_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.products_table.setAlternatingRowColors(True)
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Name column
        
        # Summary section
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        summary_layout = QHBoxLayout(summary_frame)
        
        self.total_products_label = QLabel("Total Products: 0")
        self.total_value_label = QLabel("Total Value: 0.00 DZD")
        self.low_stock_label = QLabel("Low Stock Items: 0")
        
        for label in [self.total_products_label, self.total_value_label, self.low_stock_label]:
            label.setFont(QFont("Arial", 12, QFont.Bold))
            label.setStyleSheet("color: #2c3e50;")
        
        summary_layout.addWidget(self.total_products_label)
        summary_layout.addStretch()
        summary_layout.addWidget(self.total_value_label)
        summary_layout.addStretch()
        summary_layout.addWidget(self.low_stock_label)
        
        # Add to main layout
        layout.addWidget(header_frame)
        layout.addWidget(filter_frame)
        layout.addWidget(self.products_table, 1)
        layout.addWidget(summary_frame)
        
        self.setLayout(layout)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.add_product_button.clicked.connect(self.add_product)
        self.add_category_button.clicked.connect(self.add_category)
        self.search_input.textChanged.connect(self.filter_products)
        self.category_filter.currentTextChanged.connect(self.filter_products)
        self.stock_filter.currentTextChanged.connect(self.filter_products)
        self.import_button.clicked.connect(self.import_products)
        self.export_button.clicked.connect(self.export_products)
        
    def load_category_filter(self):
        """Load categories for filter"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = cursor.fetchall()
        conn.close()
        
        for category in categories:
            self.category_filter.addItem(category['name'], category['id'])
            
    def load_products(self):
        """Load products into table"""
        products = self.db_manager.get_products()
        
        self.products_table.setRowCount(len(products))
        
        total_value = 0
        low_stock_count = 0
        
        for row, product in enumerate(products):
            # ID
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            
            # Name
            name_item = QTableWidgetItem(product['name'])
            if product['quantity'] <= 0:
                name_item.setBackground(Qt.red)
                name_item.setForeground(Qt.white)
            elif product['quantity'] <= product.get('min_quantity', 5):
                name_item.setBackground(Qt.yellow)
            self.products_table.setItem(row, 1, name_item)
            
            # Barcode
            self.products_table.setItem(row, 2, QTableWidgetItem(product.get('barcode', '')))
            
            # Category
            self.products_table.setItem(row, 3, QTableWidgetItem(product.get('category_name', '')))
            
            # Price
            self.products_table.setItem(row, 4, QTableWidgetItem(f"{product['price']:.2f} DZD"))
            
            # Cost
            cost = product.get('cost_price', 0)
            self.products_table.setItem(row, 5, QTableWidgetItem(f"{cost:.2f} DZD"))
            
            # Stock
            stock_item = QTableWidgetItem(str(product['quantity']))
            if product['quantity'] <= 0:
                stock_item.setForeground(Qt.red)
            elif product['quantity'] <= product.get('min_quantity', 5):
                stock_item.setForeground(Qt.darkYellow)
                low_stock_count += 1
            self.products_table.setItem(row, 6, stock_item)
            
            # Min Stock
            self.products_table.setItem(row, 7, QTableWidgetItem(str(product.get('min_quantity', 5))))
            
            # Actions - IMPROVED ICONS
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            
            edit_button = QPushButton("✏️ Edit")
            edit_button.setToolTip("Edit Product")
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            edit_button.clicked.connect(lambda checked, p=product: self.edit_product(p))
            
            delete_button = QPushButton("🗑️ Delete")
            delete_button.setToolTip("Delete Product")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            delete_button.clicked.connect(lambda checked, p=product: self.delete_product(p))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            self.products_table.setCellWidget(row, 8, actions_widget)
            
            # Calculate totals
            total_value += product['quantity'] * product['price']
            
        # Update summary
        self.total_products_label.setText(f"Total Products: {len(products)}")
        self.total_value_label.setText(f"Total Value: {total_value:.2f} DZD")
        self.low_stock_label.setText(f"Low Stock Items: {low_stock_count}")
        
    def filter_products(self):
        """Filter products based on search criteria"""
        search_term = self.search_input.text().lower()
        category_id = self.category_filter.currentData()
        stock_status = self.stock_filter.currentText()
        
        for row in range(self.products_table.rowCount()):
            show_row = True
            
            # Search filter
            if search_term:
                name = self.products_table.item(row, 1).text().lower()
                barcode = self.products_table.item(row, 2).text().lower()
                if search_term not in name and search_term not in barcode:
                    show_row = False
            
            # Category filter
            if category_id and show_row:
                # You'd need to implement category filtering logic here
                pass
            
            # Stock filter
            if stock_status != "All Items" and show_row:
                stock_qty = int(self.products_table.item(row, 6).text())
                min_qty = int(self.products_table.item(row, 7).text())
                
                if stock_status == "In Stock" and stock_qty <= min_qty:
                    show_row = False
                elif stock_status == "Low Stock" and (stock_qty > min_qty or stock_qty <= 0):
                    show_row = False
                elif stock_status == "Out of Stock" and stock_qty > 0:
                    show_row = False
            
            self.products_table.setRowHidden(row, not show_row)
            
    def add_product(self):
        """Add new product"""
        dialog = ProductDialog(self.db_manager, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.load_products()
            QMessageBox.information(self, "Success", "Product added successfully!")
            
    def add_category(self):
        """Add new category"""
        dialog = CategoryDialog(self.db_manager, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.load_category_filter()
            QMessageBox.information(self, "Success", "Category added successfully!")
            
    def edit_product(self, product):
        """Edit existing product"""
        dialog = ProductDialog(self.db_manager, product, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.load_products()
            QMessageBox.information(self, "Success", "Product updated successfully!")
            
    def delete_product(self, product):
        """Delete product"""
        reply = QMessageBox.question(self, "Delete Product",
                                   f"Are you sure you want to delete '{product['name']}'?\n"
                                   "This action cannot be undone.",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET is_active = 0 WHERE id = ?", (product['id'],))
                conn.commit()
                conn.close()
                
                self.load_products()
                QMessageBox.information(self, "Success", "Product deleted successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete product: {str(e)}")
                
    def import_products(self):
        """Import products from CSV"""
        QMessageBox.information(self, "Import", "Import functionality will be implemented here.")
        
    def export_products(self):
        """Export products to CSV"""
        QMessageBox.information(self, "Export", "Export functionality will be implemented here.")
