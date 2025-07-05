"""
Language Manager - Handle multi-language support
"""

from PySide6.QtCore import QObject, QTranslator, QCoreApplication

class LanguageManager(QObject):
    """Manages application languages"""
    
    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.translator = QTranslator()
        
        # Translation dictionaries (simplified - in production, use .qm files)
        self.translations = {
            "en": {
                "login": "Login",
                "username": "Username",
                "password": "Password",
                "welcome": "Welcome",
                "pos_system": "POS System",
                "point_of_sale": "Point of Sale",
                "inventory": "Inventory",
                "reports": "Reports",
                "settings": "Settings",
                "logout": "Logout",
                "add_to_cart": "Add to Cart",
                "checkout": "Checkout",
                "total": "Total",
                "cash": "Cash",
                "card": "Card",
                "print_receipt": "Print Receipt",
                "product_name": "Product Name",
                "price": "Price",
                "quantity": "Quantity",
                "barcode": "Barcode",
                "category": "Category",
                "search": "Search",
                "add_product": "Add Product",
                "edit_product": "Edit Product",
                "delete_product": "Delete Product",
                "save": "Save",
                "cancel": "Cancel",
                "yes": "Yes",
                "no": "No",
                "error": "Error",
                "success": "Success",
                "warning": "Warning",
                "information": "Information"
            },
            "ar": {
                "login": "تسجيل الدخول",
                "username": "اسم المستخدم",
                "password": "كلمة المرور",
                "welcome": "مرحباً",
                "pos_system": "نظام نقاط البيع",
                "point_of_sale": "نقطة البيع",
                "inventory": "المخزون",
                "reports": "التقارير",
                "settings": "الإعدادات",
                "logout": "تسجيل الخروج",
                "add_to_cart": "إضافة للسلة",
                "checkout": "الدفع",
                "total": "المجموع",
                "cash": "نقداً",
                "card": "بطاقة",
                "print_receipt": "طباعة الفاتورة",
                "product_name": "اسم المنتج",
                "price": "السعر",
                "quantity": "الكمية",
                "barcode": "الباركود",
                "category": "الفئة",
                "search": "بحث",
                "add_product": "إضافة منتج",
                "edit_product": "تعديل المنتج",
                "delete_product": "حذف المنتج",
                "save": "حفظ",
                "cancel": "إلغاء",
                "yes": "نعم",
                "no": "لا",
                "error": "خطأ",
                "success": "نجح",
                "warning": "تحذير",
                "information": "معلومات"
            }
        }
        
    def set_language(self, language_code):
        """Set application language"""
        self.current_language = language_code
        
        # In a full implementation, you would load .qm translation files
        # For now, we'll just store the language preference
        
    def get_text(self, key):
        """Get translated text for key"""
        return self.translations.get(self.current_language, {}).get(key, key)
        
    def is_rtl(self):
        """Check if current language is right-to-left"""
        return self.current_language == "ar"
