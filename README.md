# MOBILE ENGINEER Management System

A complete mobile engineer management system built with Flask, Python, and SQLite.

## Features

- 🔐 **Admin Login System**
- 📊 **Dashboard** with real-time statistics
- 📱 **Product Management** (Add, Edit, Delete, View Stock)
- 👥 **Customer Management** (Add and View Customers)
- 🧾 **Billing System** with automatic stock updates
- 📈 **Sales Reports** (Daily, Monthly, Top Products)
- 🎨 **Modern Responsive UI** with gradient design

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Custom CSS with modern gradients

## Installation

1. **Install Python** (3.7 or higher)

2. **Install Flask**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open in browser**: http://localhost:5000

## Default Login

- **Username**: admin
- **Password**: admin123

## Project Structure

```
mobile_engineer/
├── app.py                 # Main Flask application
├── database.db           # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── templates/           # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   ├── products.html
│   ├── add_product.html
│   ├── edit_product.html
│   ├── customers.html
│   ├── add_customer.html
│   ├── billing.html
│   ├── reports.html
│   ├── register.html
│   └── forgot_password.html
└── static/              # CSS and static files
    └── style.css
```

## Database Schema

### Products Table
- id (Primary Key)
- brand
- model
- price
- quantity
- created_at

### Customers Table
- id (Primary Key)
- name
- phone
- address
- created_at

### Sales Table
- sale_id (Primary Key)
- product_id (Foreign Key)
- customer_id (Foreign Key, Optional)
- quantity
- total_price
- sale_date

### Users Table
- id (Primary Key)
- username
- password

## Features Overview

### 1. Dashboard
- Total products count
- Total sales count
- Total customers count
- Total revenue
- Recent sales table

### 2. Product Management
- Add new mobile phones
- Edit existing products
- Delete products
- View stock levels with low-stock warnings
- Real-time stock tracking

### 3. Customer Management
- Add new customers
- View customer list
- Customer details with contact information

### 4. Billing System
- Select products for billing
- Automatic price calculation
- Stock validation
- Customer selection (optional for walk-in customers)
- Real-time stock updates after billing

### 5. Reports
- Daily sales report (last 7 days)
- Monthly sales report
- Top selling products
- Revenue analytics

## Usage Instructions

1. **Login** with admin credentials
2. **Add Products** to your inventory
3. **Add Customers** to your database
4. **Create Bills** for sales
5. **View Reports** to track business performance

## Authentication Features

- **User Registration**: Create new user accounts
- **Forgot Password**: Reset forgotten passwords
- **Secure Login**: Password hashing with salt
- **Session Management**: Secure user sessions

## Security Features

- Session-based authentication
- Input validation
- SQL injection protection
- Stock validation during billing
- Password hashing with salt

## Future Enhancements

- 🔍 Product search functionality
- 📄 Invoice PDF generation
- 📱 Barcode scanner integration
- 💳 Online payment integration
- 📊 Advanced analytics dashboard
- 👤 Multi-user support with roles

## Support

This project is designed for educational purposes and mobile engineer businesses. For support or questions, please refer to the code documentation.

---

**Happy Coding! 🚀**
