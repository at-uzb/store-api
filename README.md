# 🛒 Store API

An e-commerce RESTful API built with Django and REST Framework, designed to manage product listings, carts, orders, and users with full CRUD operations and jwt authentication.

---

## 🚀 Features

- 🔐 JWT Authentication with OTP and account deletion confirmation
- 🛍️ Product and Category CRUD
- 🔎 Search and filter products by name or category
- 🛒 Shopping cart (add, remove, update, view)
- 📦 Checkout and order tracking
- 📁 S3/Cloud support for product image uploads
- 📄 Auto-generated OpenAPI schema via Swagger (`/api/schema/`)

---

## 📦 Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- PostgreSQL
- AWS S3 (for media)
- drf-spectacular (for API docs)
- Simple JWT (for authentication)

---

## 📂 API Endpoints

### 🔐 Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/users/register/` | Register a new user |
| POST   | `/api/users/login/`    | Login and receive token |
| POST   | `/api/users/send-otp/` | Send OTP for verification |
| POST   | `/api/users/verify-otp/` | Verify OTP |
| PATCH  | `/api/users/update/`   | Update user info |
| POST   | `/api/users/delete/`   | Delete user (after OTP) |

---

### 🛍️ Products & Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/products/list/` | List products with search and filters |
| POST   | `/api/products/create/` | Create a product |
| PATCH  | `/api/products/{id}/update/` | Update product |
| DELETE | `/api/products/{id}/delete/` | Delete product |
| GET    | `/api/categories/list/` | List categories |
| POST   | `/api/categories/create/` | Create category |

---

### 🛒 Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/cart/add/` | Add item to cart |
| GET    | `/api/cart/detail/` | View cart |
| PATCH  | `/api/cart/update/{item_id}/` | Update quantity |
| DELETE | `/api/cart/remove/{item_id}/` | Remove item |

---

### 📦 Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/orders/checkout/` | Create an order from cart |
| GET    | `/api/orders/` | List user's orders |
| GET    | `/api/orders/{order_id}/` | Get order detail |

---

## 🧪 Running Locally

```bash
git clone https://github.com/your-username/store-api.git
cd store-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
