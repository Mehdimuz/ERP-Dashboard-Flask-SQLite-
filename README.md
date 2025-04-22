# 🧾 ERP Dashboard (Flask + SQLite)

A lightweight, full-featured Enterprise Resource Planning (ERP) system built using **Python Flask** and **SQLite**. This ERP system provides end-to-end management for inventory, products, customers, sales, suppliers, and invoices — perfect for small businesses or as a portfolio project.

![ERP Dashboard Screenshot](./dashboard.png)

---

## 🚀 Features

- 📦 **Inventory Tracking** — Add, view, and manage stock levels.
- 🛒 **Sales Orders** — Log sales transactions with customer linkage.
- 🧾 **Invoices** — Generate and view invoice records.
- 👥 **Customers & Suppliers** — Maintain address books for both.
- 🧮 **Purchasing System** — Log and view purchase orders.
- 📊 **Dashboard Analytics** — Track sales trends and inventory breakdown.
- 🔄 **REST API** — JSON endpoints for external use or integration.
- 🖥️ **Responsive UI** — Built using Bootstrap 5.

---

## 🖼️ Screenshots

<img src="screenshots/dashboard.png" width="800"/>
<img src="screenshots/customers.png" width="800"/>
<img src="screenshots/sales.png" width="800"/>

---

## 📁 Project Structure

erp-web/
│
├── app/
│   ├── __init__.py
│   ├── routes.py            # All HTML and API routes
│   ├── models.py            # SQLAlchemy database models
│   ├── templates/           # HTML templates (Jinja2)
│   └── static/              # Bootstrap CSS, custom JS (optional)
│
├── migrations/              # Flask-Migrate versioning files
├── run.py                   # App runner
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation


---

## 🛠️ Technologies Used

- **Backend:** Flask, SQLAlchemy
- **Frontend:** HTML, Bootstrap 5, Jinja2
- **Database:** SQLite
- **Dev Tools:** Flask-Migrate, Postman, VSCode

---

## 🔌 API Endpoints (JSON)

| Category      | Method | Endpoint              | Description              |
|---------------|--------|-----------------------|--------------------------|
| Products      | GET    | `/products`           | Get all products         |
|               | POST   | `/products`           | Add a product            |
| Inventory     | GET    | `/inventory`          | Get all inventory items  |
|               | POST   | `/inventory`          | Add inventory item       |
| Sales         | GET    | `/sales`              | Get all sales            |
|               | POST   | `/sales`              | Create a sale            |
| Customers     | GET    | `/customers`          | Get all customers        |
|               | POST   | `/customers`          | Add a customer           |
| Invoices      | GET    | `/invoices`           | Get all invoices         |
|               | POST   | `/invoices`           | Add an invoice           |
| Suppliers     | GET    | `/suppliers`          | Get all suppliers        |
|               | POST   | `/suppliers`          | Add a supplier           |
| Purchases     | GET    | `/purchase-orders`    | Get all purchase orders  |
|               | POST   | `/purchase-orders`    | Create a purchase order  |

---

## 🧪 Sample JSON for Testing

```json
POST /products
{
  "product_id": "P1001",
  "name": "Widget Pro",
  "category": "Gadgets",
  "unit_price": 19.99,
  "supplier_id": "S001",
  "stock_qty": 100
}

POST /inventory
{
  "product_id": "P1001",
  "quantity": 25,
  "location": "Warehouse A",
  "date_added": "2025-04-22"
}


🧠 Next Milestones
 Add authentication (Flask-Login)

 PDF invoice download support

 Auto-purchase on low inventory

 Search & filtering in dashboard

