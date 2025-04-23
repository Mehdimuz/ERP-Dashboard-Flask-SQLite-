from app.extensions import db
from datetime import date

# --------------------
# 📦 PRODUCT MODEL
# --------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    unit_price = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    stock_qty = db.Column(db.Integer)

    inventory_items = db.relationship('Inventory', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.product_id} - {self.name}>"

# --------------------
# 📦 INVENTORY MODEL
# --------------------
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer)
    date_added = db.Column(db.Date, default=date.today)
    location = db.Column(db.String(100))

    def __repr__(self):
        return f"<Inventory for {self.product_id} - Qty: {self.quantity}>"

# --------------------
# 🛒 SALES MODELS
# --------------------
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), unique=True)
    date = db.Column(db.Date, default=date.today)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    total = db.Column(db.Float)

    items = db.relationship('SaleItem', backref='sale', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f"<Sale #{self.order_id} - Total: {self.total}>"

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'))
    product_id = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)

    def __repr__(self):
        return f"<SaleItem {self.product_id} - Qty: {self.quantity}>"

# --------------------
# 📥 PURCHASE MODELS
# --------------------
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(50), unique=True)
    date = db.Column(db.Date, default=date.today)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    total = db.Column(db.Float)

    items = db.relationship('PurchaseItem', backref='purchase', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f"<Purchase #{self.po_number} - Total: {self.total}>"

class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    product_id = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)

    def __repr__(self):
        return f"<PurchaseItem {self.product_id} - Qty: {self.quantity}>"

# --------------------
# 👥 CUSTOMER MODEL
# --------------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

    sales = db.relationship('Sale', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"

# --------------------
# 🧾 INVOICE MODEL
# --------------------
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))  # e.g., Paid, Pending
    due_date = db.Column(db.Date)

    def __repr__(self):
        return f"<Invoice #{self.invoice_number} - Status: {self.status}>"

# --------------------
# 🚚 SUPPLIER MODEL
# --------------------
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    address = db.Column(db.String(200))

    products = db.relationship('Product', backref='supplier', lazy=True)
    purchases = db.relationship('Purchase', backref='supplier', lazy=True)

    def __repr__(self):
        return f"<Supplier {self.name}>"
