# Srinivas-press-tools
flask web app for managing production, sales and steel inventory for a manufacturing business
 Srinivaass Press Tools
Manufacturing Management System

A full-stack web application to manage production, sales, and raw material procurement for a small press tool manufacturing company.


📋 Table of Contents

About the Project
Tech Stack
Features
Project Structure
Getting Started
Usage Guide
Sample Data
Database Schema


🏭 About the Project
Srinivaass Press Tools is a beginner-friendly, fully functional web application designed for a small manufacturing business. The company:

Buys raw steel from suppliers
Manufactures metal components using press tools
Sells finished components to customers

This system helps track all three stages — raw material purchases, production output, and customer sales — with a visual dashboard showing key business insights.

🛠️ Tech Stack
LayerTechnologyBackendPython 3.8+ · Flask 3.0DatabaseSQLite (zero configuration needed)FrontendHTML5 · Bootstrap 5.3 · Bootstrap IconsChartsChart.js 4.4TemplatingJinja2 (built into Flask)

✨ Features
📦 Production Entry

Log daily manufacturing output by product name
Track pieces produced per date
View full history in a sortable table

💰 Sales Entry

Record customer orders with product and quantity
Auto-calculates total amount (Quantity × Price per piece) in real time
Full sales history with revenue per transaction

🔩 Steel Purchase

Log raw steel procurement from suppliers
Auto-calculates rate per kg for easy cost comparison
Track total material spend over time

📊 Dashboard

4 KPI cards: Total production, total revenue, steel purchased (kg), steel cost
Insights panel: Most produced product, most sold product
Top products bar: Visual progress bars for top 5 products by volume
Revenue chart: Monthly revenue trend (Bar chart via Chart.js)
Production chart: Monthly output trend (Line chart via Chart.js)

🎨 UI & UX

Clean, mobile-responsive layout (Bootstrap 5)
Sticky navigation bar with active page highlighting
Flash messages on every form submission (success / error)
Client-side and server-side form validation
Animated spinning gear logo


📁 Project Structure
srinivaass_press_tools/
│
├── app.py                  ← Main Flask app (routes, DB logic, validation)
├── requirements.txt        ← Python dependencies (just Flask)
├── database.db             ← SQLite DB (auto-created on first run)
├── README.md               ← This file
│
├── templates/              ← Jinja2 HTML templates
│   ├── base.html           ← Shared layout: navbar, flash messages, footer
│   ├── home.html           ← Landing page with module cards
│   ├── production.html     ← Production entry form + records table
│   ├── sales.html          ← Sales entry form + records table
│   ├── steel.html          ← Steel purchase form + records table
│   └── dashboard.html      ← KPIs, insights, and Chart.js charts
│
└── static/
    └── css/
        └── style.css       ← Custom styles (colors, cards, animations)

🚀 Getting Started
Prerequisites

Python 3.8 or higher
pip (Python package manager)

Check your Python version:
bashpython --version

Step 1 — Extract the Project
Unzip the downloaded file and navigate into the project folder:
bashcd srinivaass_press_tools

Step 2 — Create a Virtual Environment (Recommended)
bashpython -m venv venv
Activate it:
On Windows:
bashvenv\Scripts\activate
On macOS / Linux:
bashsource venv/bin/activate
You'll see (venv) in your terminal prompt when it's active.

Step 3 — Install Dependencies
bashpip install -r requirements.txt
This installs Flask. SQLite and Jinja2 come built into Python — no extra installs needed.

Step 4 — Run the Application
bashpython app.py
You should see output like:
 * Running on http://127.0.0.1:5000
 * Debug mode: on

Step 5 — Open in Your Browser
Visit: http://127.0.0.1:5000
The database (database.db) is automatically created on the very first run. No manual setup needed!
