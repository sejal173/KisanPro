# KisanPro – Folder Structure Explained

## Overview

```
KisanPro/
├── app.py                    # Main Flask application (backend)
├── requirements.txt         # Python dependencies
├── setup_database.py        # Database setup script
├── database_setup.sql       # Raw SQL for manual DB setup
├── init_admin.py            # Create admin account
├── create_admin.py          # Alternative admin creation script
├── .gitignore               # Files to ignore in Git
├── README.md                # Full project documentation
├── QUICK_START.md           # Quick start guide
├── SETUP_GUIDE.md           # Setup instructions
├── DATABASE_CONNECTED.md    # DB connection info
├── templates/               # HTML pages (frontend)
└── static/                  # CSS, JS, images
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

---

## Root folder (KisanPro/)

| File / Folder | Purpose |
|---------------|--------|
| **app.py** | Main Flask app. All routes (URLs), database logic, farmer/admin login, seeds, cart, orders. This is the backend. |
| **requirements.txt** | List of Python packages (Flask, PyMySQL, etc.). Used by `pip install -r requirements.txt`. |
| **setup_database.py** | Script that creates the database, tables, default admin, and sample seeds. Run once after installing MySQL. |
| **database_setup.sql** | Same schema in plain SQL. Use if you prefer to run SQL manually in MySQL. |
| **init_admin.py** | Creates the default admin (admin@kisanpro.com). Use if you need to recreate only the admin. |
| **create_admin.py** | Another script to create an admin; asks for name, email, password. |
| **.gitignore** | Tells Git which files/folders not to track (e.g. `__pycache__`, `.env`, virtual env). |
| **README.md** | Full project documentation. |
| **QUICK_START.md** | Short steps to run the project. |
| **SETUP_GUIDE.md** | Detailed setup (MySQL, config, troubleshooting). |
| **DATABASE_CONNECTED.md** | Notes after DB is connected and app is running. |

---

## templates/ – HTML pages

Flask uses these to render each page. All extend **base.html** for same navbar and layout.

| File | Purpose |
|------|----------|
| **base.html** | Layout template: navbar, footer, flash messages. Other pages extend this. |
| **home.html** | Home page: welcome, featured seeds, “Browse Seeds” / “Register”. |
| **farmer_login.html** | Farmer login form (email, password). |
| **farmer_register.html** | Farmer registration (name, email, password, contact, address). |
| **admin_login.html** | Admin login form. |
| **seeds_list.html** | List of seeds with filters (crop type, season). |
| **seed_details.html** | Single seed: name, type, season, price, stock, description, “Add to cart”. |
| **cart.html** | Cart: items, quantity, total, “Place order”. |
| **orders.html** | Farmer’s order history (list of orders). |
| **order_details.html** | One order: items, quantities, total, status. |
| **admin_dashboard.html** | Admin home: stats (seeds, orders, farmers, pending). |
| **admin_seeds.html** | Admin: list seeds, Edit/Delete. |
| **admin_seed_form.html** | Admin: add or edit seed (name, type, season, price, stock, description). |
| **admin_orders.html** | Admin: list orders, filter by status, change status. |
| **admin_farmers.html** | Admin: list farmers, Delete. |
| **about.html** | About page. |
| **contact.html** | Contact page (info + contact form). |

---

## static/ – CSS and JavaScript

Files here are served as-is (no Jinja). Used for styling and behavior.

| Path | Purpose |
|------|--------|
| **static/css/style.css** | All styles: navbar, buttons, cards, forms, tables, responsive layout, colors. |
| **static/js/main.js** | Mobile menu, flash message auto-hide, form validation, cart quantity checks, etc. |

---

## How it fits together

1. **User visits a URL** (e.g. `/seeds`, `/cart`).
2. **app.py** has a route for that URL; it may read/write the database (MySQL via PyMySQL).
3. **app.py** calls `render_template('some_page.html', ...)` and passes data.
4. **templates/some_page.html** uses that data and extends **base.html**.
5. **base.html** includes `static/css/style.css` and `static/js/main.js`, so every page gets the same look and behavior.

---

## Summary

| Part | Role |
|------|------|
| **app.py** | Backend: routes, database, auth. |
| **templates/** | Frontend: every HTML page. |
| **static/css/** | Styling. |
| **static/js/** | Interactivity. |
| **setup_database.py** | One-time DB + admin + sample data. |
| **requirements.txt** | Python packages to install. |

This is the complete folder structure of your KisanPro project.
