"""
Reports Module - Sales analytics and reporting
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QFrame, QComboBox, QDateEdit, QTabWidget,
                              QGroupBox, QGridLayout, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from datetime import datetime, timedelta
import csv

class ReportsModule(QWidget):
    """Reports and analytics module"""
    
    def __init__(self, user, db_manager):
        super().__init__()
        self.user = user
        self.db_manager = db_manager
        self.setup_ui()
        self.setup_connections()
        self.load_default_report()
        
    def setup_ui(self):
        """Setup reports interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("📊 Reports & Analytics")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Tab widget for different report types
        self.tab_widget = QTabWidget()
        
        # Sales Report Tab
        sales_tab = self.create_sales_report_tab()
        self.tab_widget.addTab(sales_tab, "Sales Reports")
        
        # Inventory Report Tab
        inventory_tab = self.create_inventory_report_tab()
        self.tab_widget.addTab(inventory_tab, "Inventory Reports")
        
        # Summary Tab
        summary_tab = self.create_summary_tab()
        self.tab_widget.addTab(summary_tab, "Summary")
        
        # Add to main layout
        layout.addWidget(header_frame)
        layout.addWidget(self.tab_widget, 1)
        
        self.setLayout(layout)
        
    def create_sales_report_tab(self):
        """Create sales report tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Date range selection
        date_frame = QFrame()
        date_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        date_layout = QHBoxLayout(date_frame)
        
        date_layout.addWidget(QLabel("From:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("To:"))
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        date_layout.addWidget(self.end_date)
        
        self.generate_report_button = QPushButton("Generate Report")
        self.generate_report_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        self.export_report_button = QPushButton("Export to CSV")
        self.export_report_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        date_layout.addWidget(self.generate_report_button)
        date_layout.addWidget(self.export_report_button)
        date_layout.addStretch()
        
        # Sales summary cards
        summary_frame = QFrame()
        summary_layout = QHBoxLayout(summary_frame)
        
        # Total Sales Card
        total_sales_card = self.create_summary_card("Total Sales", "$0.00", "#007bff")
        summary_layout.addWidget(total_sales_card)
        
        # Total Transactions Card
        total_transactions_card = self.create_summary_card("Transactions", "0", "#28a745")
        summary_layout.addWidget(total_transactions_card)
        
        # Average Sale Card
        avg_sale_card = self.create_summary_card("Avg. Sale", "$0.00", "#ffc107")
        summary_layout.addWidget(avg_sale_card)
        
        # Profit Card
        profit_card = self.create_summary_card("Profit", "$0.00", "#17a2b8")
        summary_layout.addWidget(profit_card)
        
        # Sales table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels([
            "Sale #", "Date", "Cashier", "Items", "Subtotal", "Tax", "Total"
        ])
        
        self.sales_table.setStyleSheet("""
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
        """)
        
        layout.addWidget(date_frame)
        layout.addWidget(summary_frame)
        layout.addWidget(self.sales_table, 1)
        
        return tab
        
    def create_inventory_report_tab(self):
        """Create inventory report tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Inventory summary
        summary_frame = QFrame()
        summary_layout = QHBoxLayout(summary_frame)
        
        # Total Products Card
        total_products_card = self.create_summary_card("Total Products", "0", "#6f42c1")
        summary_layout.addWidget(total_products_card)
        
        # Low Stock Card
        low_stock_card = self.create_summary_card("Low Stock", "0", "#dc3545")
        summary_layout.addWidget(low_stock_card)
        
        # Out of Stock Card
        out_stock_card = self.create_summary_card("Out of Stock", "0", "#fd7e14")
        summary_layout.addWidget(out_stock_card)
        
        # Total Value Card
        total_value_card = self.create_summary_card("Total Value", "$0.00", "#20c997")
        summary_layout.addWidget(total_value_card)
        
        # Inventory table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels([
            "Product", "Category", "Current Stock", "Min Stock", "Value", "Status"
        ])
        
        self.inventory_table.setStyleSheet("""
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
        """)
        
        layout.addWidget(summary_frame)
        layout.addWidget(self.inventory_table, 1)
        
        return tab
        
    def create_summary_tab(self):
        """Create summary dashboard tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Quick stats
        stats_frame = QFrame()
        stats_layout = QGridLayout(stats_frame)
        
        # Today's sales
        today_frame = QGroupBox("Today's Performance")
        today_layout = QVBoxLayout(today_frame)
        
        self.today_sales_label = QLabel("Sales: $0.00")
        self.today_transactions_label = QLabel("Transactions: 0")
        self.today_items_label = QLabel("Items Sold: 0")
        
        for label in [self.today_sales_label, self.today_transactions_label, self.today_items_label]:
            label.setFont(QFont("Arial", 12))
            label.setStyleSheet("color: #2c3e50; margin: 5px;")
            today_layout.addWidget(label)
        
        # This week's sales
        week_frame = QGroupBox("This Week's Performance")
        week_layout = QVBoxLayout(week_frame)
        
        self.week_sales_label = QLabel("Sales: $0.00")
        self.week_transactions_label = QLabel("Transactions: 0")
        self.week_avg_label = QLabel("Daily Average: $0.00")
        
        for label in [self.week_sales_label, self.week_transactions_label, self.week_avg_label]:
            label.setFont(QFont("Arial", 12))
            label.setStyleSheet("color: #2c3e50; margin: 5px;")
            week_layout.addWidget(label)
        
        # This month's sales
        month_frame = QGroupBox("This Month's Performance")
        month_layout = QVBoxLayout(month_frame)
        
        self.month_sales_label = QLabel("Sales: $0.00")
        self.month_transactions_label = QLabel("Transactions: 0")
        self.month_growth_label = QLabel("Growth: 0%")
        
        for label in [self.month_sales_label, self.month_transactions_label, self.month_growth_label]:
            label.setFont(QFont("Arial", 12))
            label.setStyleSheet("color: #2c3e50; margin: 5px;")
            month_layout.addWidget(label)
        
        stats_layout.addWidget(today_frame, 0, 0)
        stats_layout.addWidget(week_frame, 0, 1)
        stats_layout.addWidget(month_frame, 0, 2)
        
        # Recent activity
        activity_frame = QGroupBox("Recent Activity")
        activity_layout = QVBoxLayout(activity_frame)
        
        self.activity_text = QTextEdit()
        self.activity_text.setReadOnly(True)
        self.activity_text.setMaximumHeight(200)
        self.activity_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        activity_layout.addWidget(self.activity_text)
        
        layout.addWidget(stats_frame)
        layout.addWidget(activity_frame)
        layout.addStretch()
        
        return tab
        
    def create_summary_card(self, title, value, color):
        """Create a summary card widget"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                color: white;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 18, QFont.Bold))
        value_label.setStyleSheet("color: white;")
        
        # Store reference to value label for updates
        setattr(self, f"{title.lower().replace(' ', '_').replace('.', '')}_value_label", value_label)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
        
    def setup_connections(self):
        """Setup signal connections"""
        self.generate_report_button.clicked.connect(self.generate_sales_report)
        self.export_report_button.clicked.connect(self.export_sales_report)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
    def load_default_report(self):
        """Load default report data"""
        self.generate_sales_report()
        self.load_inventory_report()
        self.load_summary_data()
        
    def generate_sales_report(self):
        """Generate sales report for selected date range"""
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        # Get sales data
        sales = self.db_manager.get_sales_report(start_date, end_date)
        
        # Update table
        self.sales_table.setRowCount(len(sales))
        
        total_sales = 0
        total_transactions = len(sales)
        
        for row, sale in enumerate(sales):
            self.sales_table.setItem(row, 0, QTableWidgetItem(sale['sale_number']))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale['created_at'][:10]))
            self.sales_table.setItem(row, 2, QTableWidgetItem(sale['cashier_name']))
            self.sales_table.setItem(row, 3, QTableWidgetItem("N/A"))  # Items count would need separate query
            self.sales_table.setItem(row, 4, QTableWidgetItem(f"${sale['subtotal']:.2f}"))
            self.sales_table.setItem(row, 5, QTableWidgetItem(f"${sale['tax_amount']:.2f}"))
            self.sales_table.setItem(row, 6, QTableWidgetItem(f"${sale['total_amount']:.2f}"))
            
            total_sales += sale['total_amount']
        
        # Update summary cards
        avg_sale = total_sales / total_transactions if total_transactions > 0 else 0
        
        self.total_sales_value_label.setText(f"${total_sales:.2f}")
        self.transactions_value_label.setText(str(total_transactions))
        self.avg_sale_value_label.setText(f"${avg_sale:.2f}")
        self.profit_value_label.setText("$0.00")  # Would need cost calculation
        
    def load_inventory_report(self):
        """Load inventory report data"""
        products = self.db_manager.get_products()
        
        self.inventory_table.setRowCount(len(products))
        
        total_products = len(products)
        low_stock_count = 0
        out_of_stock_count = 0
        total_value = 0
        
        for row, product in enumerate(products):
            self.inventory_table.setItem(row, 0, QTableWidgetItem(product['name']))
            self.inventory_table.setItem(row, 1, QTableWidgetItem(product.get('category_name', '')))
            self.inventory_table.setItem(row, 2, QTableWidgetItem(str(product['quantity'])))
            self.inventory_table.setItem(row, 3, QTableWidgetItem(str(product.get('min_quantity', 5))))
            
            value = product['quantity'] * product['price']
            self.inventory_table.setItem(row, 4, QTableWidgetItem(f"${value:.2f}"))
            
            # Status
            if product['quantity'] <= 0:
                status = "Out of Stock"
                out_of_stock_count += 1
            elif product['quantity'] <= product.get('min_quantity', 5):
                status = "Low Stock"
                low_stock_count += 1
            else:
                status = "In Stock"
                
            status_item = QTableWidgetItem(status)
            if status == "Out of Stock":
                status_item.setForeground(Qt.red)
            elif status == "Low Stock":
                status_item.setForeground(Qt.darkYellow)
            else:
                status_item.setForeground(Qt.darkGreen)
                
            self.inventory_table.setItem(row, 5, status_item)
            
            total_value += value
        
        # Update inventory summary cards
        self.total_products_value_label.setText(str(total_products))
        self.low_stock_value_label.setText(str(low_stock_count))
        self.out_of_stock_value_label.setText(str(out_of_stock_count))
        self.total_value_value_label.setText(f"${total_value:.2f}")
        
    def load_summary_data(self):
        """Load summary dashboard data"""
        today = datetime.now().strftime("%Y-%m-%d")
        week_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        month_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Today's data
        today_sales = self.db_manager.get_sales_report(today, today)
        today_total = sum(sale['total_amount'] for sale in today_sales)
        
        self.today_sales_label.setText(f"Sales: ${today_total:.2f}")
        self.today_transactions_label.setText(f"Transactions: {len(today_sales)}")
        self.today_items_label.setText("Items Sold: N/A")  # Would need separate calculation
        
        # Week's data
        week_sales = self.db_manager.get_sales_report(week_start, today)
        week_total = sum(sale['total_amount'] for sale in week_sales)
        week_avg = week_total / 7
        
        self.week_sales_label.setText(f"Sales: ${week_total:.2f}")
        self.week_transactions_label.setText(f"Transactions: {len(week_sales)}")
        self.week_avg_label.setText(f"Daily Average: ${week_avg:.2f}")
        
        # Month's data
        month_sales = self.db_manager.get_sales_report(month_start, today)
        month_total = sum(sale['total_amount'] for sale in month_sales)
        
        self.month_sales_label.setText(f"Sales: ${month_total:.2f}")
        self.month_transactions_label.setText(f"Transactions: {len(month_sales)}")
        self.month_growth_label.setText("Growth: N/A")  # Would need previous month comparison
        
        # Recent activity
        self.load_recent_activity()
        
    def load_recent_activity(self):
        """Load recent activity log"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT al.*, u.full_name
            FROM activity_logs al
            JOIN users u ON al.user_id = u.id
            ORDER BY al.created_at DESC
            LIMIT 10
        ''')
        
        activities = cursor.fetchall()
        conn.close()
        
        activity_text = ""
        for activity in activities:
            timestamp = activity['created_at'][:19]  # Remove microseconds
            activity_text += f"[{timestamp}] {activity['full_name']}: {activity['action']}\n"
            if activity['details']:
                activity_text += f"  → {activity['details']}\n"
            activity_text += "\n"
        
        self.activity_text.setPlainText(activity_text)
        
    def export_sales_report(self):
        """Export sales report to CSV"""
        try:
            from PySide6.QtWidgets import QFileDialog
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Sales Report", 
                f"sales_report_{datetime.now().strftime('%Y%m%d')}.csv",
                "CSV Files (*.csv)"
            )
            
            if file_path:
                start_date = self.start_date.date().toString("yyyy-MM-dd")
                end_date = self.end_date.date().toString("yyyy-MM-dd")
                sales = self.db_manager.get_sales_report(start_date, end_date)
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Sale Number', 'Date', 'Cashier', 'Subtotal', 'Tax', 'Total'])
                    
                    for sale in sales:
                        writer.writerow([
                            sale['sale_number'],
                            sale['created_at'][:10],
                            sale['cashier_name'],
                            sale['subtotal'],
                            sale['tax_amount'],
                            sale['total_amount']
                        ])
                
                QMessageBox.information(self, "Export Successful", 
                                      f"Sales report exported to:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export report: {str(e)}")
            
    def on_tab_changed(self, index):
        """Handle tab change"""
        if index == 1:  # Inventory tab
            self.load_inventory_report()
        elif index == 2:  # Summary tab
            self.load_summary_data()
