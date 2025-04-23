from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models import Product, Inventory, Sale, SaleItem, Customer, Invoice, Supplier, Purchase, PurchaseItem
from app.extensions import db
from collections import defaultdict
from datetime import datetime, date

main_bp = Blueprint('main', __name__)

# ---- API ENDPOINTS ----

@main_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "product_id": p.product_id,
        "name": p.name,
        "category": p.category,
        "unit_price": p.unit_price,
        "supplier_id": p.supplier_id,
        "stock_qty": p.stock_qty
    } for p in products])

@main_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product added!', 'product': data}), 201

@main_bp.route('/products/view')
def view_products_page():
    products = Product.query.all()
    return render_template('products.html', products=products, title='Products')

@main_bp.route('/inventory', methods=['GET'])
def get_inventory():
    items = Inventory.query.all()
    return jsonify([{
        "product_id": item.product_id,
        "quantity": item.quantity,
        "date_added": item.date_added.strftime("%Y-%m-%d") if item.date_added else None,
        "location": item.location,
        "product_name": item.product.name if item.product else None,
        "category": item.product.category if item.product else None,
        "unit_price": item.product.unit_price if item.product else None
    } for item in items])

@main_bp.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()

    if "date_added" in data:
        try:
            data["date_added"] = datetime.strptime(data["date_added"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    item = Inventory(
        product_id=data["product_id"],
        quantity=data["quantity"],
        date_added=data.get("date_added", date.today()),
        location=data.get("location", "Unknown")
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({'message': 'Inventory item added!', 'inventory': {
        "product_id": item.product_id,
        "quantity": item.quantity,
        "date_added": item.date_added.strftime("%Y-%m-%d"),
        "location": item.location
    }}), 201

@main_bp.route('/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    return jsonify([{
        "order_id": s.order_id,
        "date": s.date.strftime("%Y-%m-%d") if s.date else None,
        "customer_id": s.customer_id,
        "total": s.total
    } for s in sales])

@main_bp.route('/sales', methods=['POST'])
def create_sale():
    data = request.get_json()
    try:
        sale_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    except:
        sale_date = date.today()

    sale = Sale(
        order_id=data['order_id'],
        date=sale_date,
        customer_id=data['customer_id'],
        total=data['total']
    )
    db.session.add(sale)
    db.session.commit()
    return jsonify({'message': 'Sale created!', 'sale': data}), 201

@main_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "address": c.address
    } for c in customers])

@main_bp.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer added!', 'customer': data}), 201

@main_bp.route('/customers/view')
def view_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers, title='Customers')

@main_bp.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([{
        "invoice_number": inv.invoice_number,
        "sale_id": inv.sale_id,
        "amount": inv.amount,
        "status": inv.status,
        "due_date": inv.due_date.strftime("%Y-%m-%d") if inv.due_date else None
    } for inv in invoices])

@main_bp.route('/invoices', methods=['POST'])
def add_invoice():
    data = request.get_json()

    if "due_date" in data:
        try:
            data["due_date"] = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Use YYYY-MM-DD."}), 400

    invoice = Invoice(**data)
    db.session.add(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice added!', 'invoice': data}), 201

@main_bp.route('/invoices/view')
def view_invoices():
    invoices = Invoice.query.all()
    return render_template('invoices.html', invoices=invoices, title='Invoices')

@main_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{
        "id": s.id,
        "supplier_id": s.supplier_id,
        "name": s.name,
        "contact": s.contact,
        "address": s.address
    } for s in suppliers])

@main_bp.route('/suppliers', methods=['POST'])
def add_supplier():
    data = request.get_json()
    supplier = Supplier(**data)
    db.session.add(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier added!', 'supplier': data}), 201

@main_bp.route('/suppliers/view')
def view_suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers, title='Suppliers')

@main_bp.route('/purchase-orders', methods=['POST'])
def add_purchase():
    data = request.get_json()

    try:
        purchase_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    except:
        purchase_date = date.today()

    purchase = Purchase(
        po_number=data['po_number'],
        date=purchase_date,
        supplier_id=data['supplier_id'],
        total=data['total']
    )
    db.session.add(purchase)
    db.session.commit()
    return jsonify({'message': 'Purchase order added!', 'purchase': data}), 201

@main_bp.route('/purchase-orders', methods=['GET'])
def get_purchases():
    purchases = Purchase.query.all()
    return jsonify([{
        "po_number": p.po_number,
        "date": p.date.strftime("%Y-%m-%d") if p.date else None,
        "supplier_id": p.supplier_id,
        "total": p.total
    } for p in purchases])

# ---- HTML ROUTES ----

@main_bp.route('/')
def index():
    sales = Sale.query.all()
    inventory = Inventory.query.all()
    customers = Customer.query.all()
    invoices = Invoice.query.all()
    products = Product.query.all()

    total_sales = len(sales)
    total_products = len(products)
    total_customers = len(customers)
    total_invoices = len(invoices)

    monthly_sales = [0] * 12
    for s in sales:
        try:
            month = s.date.month
            monthly_sales[month - 1] += 1
        except Exception:
            pass

    category_counts = defaultdict(int)
    for i in inventory:
        if i.product and i.product.category:
            category_counts[i.product.category] += 1
        else:
            category_counts["Uncategorized"] += 1

    inventory_labels = list(category_counts.keys())
    inventory_data = list(category_counts.values())

    return render_template('index.html',
        title='ERP Dashboard',
        total_sales=total_sales,
        total_products=total_products,
        total_customers=total_customers,
        total_invoices=total_invoices,
        monthly_sales=monthly_sales,
        inventory_labels=inventory_labels,
        inventory_data=inventory_data)

@main_bp.route('/purchase-orders/view')
def view_purchase_orders():
    return render_template('purchase_orders.html', title='Purchase Orders')

@main_bp.route('/sales/view')
def view_sales():
    sales = Sale.query.all()
    return render_template('sales.html', sales=sales, title='Sales Orders')

@main_bp.route('/restocking/view')
def view_restocking():
    return render_template('restocking.html', title='Supplier Restocking')

@main_bp.route('/inventory/view')
def view_inventory():
    items = Inventory.query.all()
    return render_template('inventory.html', inventory=items, title='Inventory Overview')

@main_bp.route('/sales/new', methods=['GET', 'POST'])
def new_sale():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        date_val = request.form.get('date')

        try:
            parsed_date = datetime.strptime(date_val, "%Y-%m-%d").date()
        except:
            parsed_date = date.today()

        customer_id = 1
        sale = Sale(order_id=f"SO{len(Sale.query.all())+1}", date=parsed_date, customer_id=customer_id, total=0)
        db.session.add(sale)
        db.session.flush()

        item = SaleItem(sale_id=sale.id, product_id=product_id, quantity=quantity, unit_price=0)
        db.session.add(item)
        db.session.commit()

        return render_template('sale_success.html', sale=item)

    return render_template('new_sale.html')
