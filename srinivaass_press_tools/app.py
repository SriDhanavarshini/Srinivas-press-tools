# ============================================================
# app.py - Main Flask Application for Srinivaass Press Tools
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'srinivaass_press_tools_secret_2024'  # Required for flash messages

# Path to the SQLite database file
DATABASE = 'database.db'


# ─────────────────────────────────────────────
# DATABASE HELPERS
# ─────────────────────────────────────────────

def get_db():
    """Open a new database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    # Production table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS production (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            date      TEXT    NOT NULL,
            product   TEXT    NOT NULL,
            pieces    INTEGER NOT NULL
        )
    ''')

    # Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            date          TEXT    NOT NULL,
            customer      TEXT    NOT NULL,
            product       TEXT    NOT NULL,
            quantity      INTEGER NOT NULL,
            price_per_pc  REAL    NOT NULL,
            total_amount  REAL    NOT NULL
        )
    ''')

    # Steel purchases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS steel_purchases (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            date         TEXT    NOT NULL,
            supplier     TEXT    NOT NULL,
            quantity_kg  REAL    NOT NULL,
            cost         REAL    NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# HOME / LANDING PAGE
# ─────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html')


# ─────────────────────────────────────────────
# PRODUCTION ROUTES
# ─────────────────────────────────────────────

@app.route('/production', methods=['GET', 'POST'])
def production():
    """Show and handle the production entry form."""
    if request.method == 'POST':
        date    = request.form.get('date', '').strip()
        product = request.form.get('product', '').strip()
        pieces  = request.form.get('pieces', '').strip()

        # Basic validation
        if not date or not product or not pieces:
            flash('All fields are required!', 'danger')
            return redirect(url_for('production'))

        try:
            pieces = int(pieces)
            if pieces <= 0:
                raise ValueError
        except ValueError:
            flash('Pieces must be a positive whole number.', 'danger')
            return redirect(url_for('production'))

        conn = get_db()
        conn.execute(
            'INSERT INTO production (date, product, pieces) VALUES (?, ?, ?)',
            (date, product, pieces)
        )
        conn.commit()
        conn.close()
        flash(f'Production entry saved! {pieces} pieces of "{product}" recorded.', 'success')
        return redirect(url_for('production'))

    # GET: load all production records (newest first)
    conn = get_db()
    records = conn.execute(
        'SELECT * FROM production ORDER BY date DESC'
    ).fetchall()
    conn.close()
    return render_template('production.html', records=records)


# ─────────────────────────────────────────────
# SALES ROUTES
# ─────────────────────────────────────────────

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    """Show and handle the sales entry form."""
    if request.method == 'POST':
        date        = request.form.get('date', '').strip()
        customer    = request.form.get('customer', '').strip()
        product     = request.form.get('product', '').strip()
        quantity    = request.form.get('quantity', '').strip()
        price_per_pc = request.form.get('price_per_pc', '').strip()

        if not all([date, customer, product, quantity, price_per_pc]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('sales'))

        try:
            quantity     = int(quantity)
            price_per_pc = float(price_per_pc)
            if quantity <= 0 or price_per_pc <= 0:
                raise ValueError
        except ValueError:
            flash('Quantity and price must be positive numbers.', 'danger')
            return redirect(url_for('sales'))

        total_amount = quantity * price_per_pc

        conn = get_db()
        conn.execute(
            '''INSERT INTO sales
               (date, customer, product, quantity, price_per_pc, total_amount)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (date, customer, product, quantity, price_per_pc, total_amount)
        )
        conn.commit()
        conn.close()
        flash(f'Sale recorded! ₹{total_amount:,.2f} from {customer}.', 'success')
        return redirect(url_for('sales'))

    conn = get_db()
    records = conn.execute(
        'SELECT * FROM sales ORDER BY date DESC'
    ).fetchall()
    conn.close()
    return render_template('sales.html', records=records)


# ─────────────────────────────────────────────
# STEEL PURCHASE ROUTES
# ─────────────────────────────────────────────

@app.route('/steel', methods=['GET', 'POST'])
def steel():
    """Show and handle the steel purchase entry form."""
    if request.method == 'POST':
        date        = request.form.get('date', '').strip()
        supplier    = request.form.get('supplier', '').strip()
        quantity_kg = request.form.get('quantity_kg', '').strip()
        cost        = request.form.get('cost', '').strip()

        if not all([date, supplier, quantity_kg, cost]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('steel'))

        try:
            quantity_kg = float(quantity_kg)
            cost        = float(cost)
            if quantity_kg <= 0 or cost <= 0:
                raise ValueError
        except ValueError:
            flash('Quantity and cost must be positive numbers.', 'danger')
            return redirect(url_for('steel'))

        conn = get_db()
        conn.execute(
            'INSERT INTO steel_purchases (date, supplier, quantity_kg, cost) VALUES (?, ?, ?, ?)',
            (date, supplier, quantity_kg, cost)
        )
        conn.commit()
        conn.close()
        flash(f'Steel purchase saved! {quantity_kg} kg from {supplier}.', 'success')
        return redirect(url_for('steel'))

    conn = get_db()
    records = conn.execute(
        'SELECT * FROM steel_purchases ORDER BY date DESC'
    ).fetchall()
    conn.close()
    return render_template('steel.html', records=records)


# ─────────────────────────────────────────────
# DASHBOARD ROUTE
# ─────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    """Aggregate stats and insights for the dashboard."""
    conn = get_db()

    # ── Summary cards ──
    total_production = conn.execute(
        'SELECT COALESCE(SUM(pieces), 0) FROM production'
    ).fetchone()[0]

    total_revenue = conn.execute(
        'SELECT COALESCE(SUM(total_amount), 0) FROM sales'
    ).fetchone()[0]

    total_steel_kg = conn.execute(
        'SELECT COALESCE(SUM(quantity_kg), 0) FROM steel_purchases'
    ).fetchone()[0]

    total_steel_cost = conn.execute(
        'SELECT COALESCE(SUM(cost), 0) FROM steel_purchases'
    ).fetchone()[0]

    # ── Insights ──
    most_produced = conn.execute(
        '''SELECT product, SUM(pieces) AS total
           FROM production
           GROUP BY product
           ORDER BY total DESC
           LIMIT 1'''
    ).fetchone()

    most_sold = conn.execute(
        '''SELECT product, SUM(quantity) AS total
           FROM sales
           GROUP BY product
           ORDER BY total DESC
           LIMIT 1'''
    ).fetchone()

    # ── Monthly revenue for Chart.js (last 6 months) ──
    monthly_revenue = conn.execute(
        '''SELECT strftime('%Y-%m', date) AS month,
                  ROUND(SUM(total_amount), 2) AS revenue
           FROM sales
           GROUP BY month
           ORDER BY month DESC
           LIMIT 6'''
    ).fetchall()
    # Reverse so chart shows oldest → newest
    monthly_revenue = list(reversed(monthly_revenue))

    # ── Monthly production trend ──
    monthly_production = conn.execute(
        '''SELECT strftime('%Y-%m', date) AS month,
                  SUM(pieces) AS pieces
           FROM production
           GROUP BY month
           ORDER BY month DESC
           LIMIT 6'''
    ).fetchall()
    monthly_production = list(reversed(monthly_production))

    # ── Top 5 products by production ──
    top_products = conn.execute(
        '''SELECT product, SUM(pieces) AS total
           FROM production
           GROUP BY product
           ORDER BY total DESC
           LIMIT 5'''
    ).fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        total_production   = total_production,
        total_revenue      = total_revenue,
        total_steel_kg     = total_steel_kg,
        total_steel_cost   = total_steel_cost,
        most_produced      = most_produced,
        most_sold          = most_sold,
        monthly_revenue    = monthly_revenue,
        monthly_production = monthly_production,
        top_products       = top_products,
    )


# ─────────────────────────────────────────────
# SAMPLE DATA LOADER (dev helper)
# ─────────────────────────────────────────────

@app.route('/load_sample_data')
def load_sample_data():
    """Load sample data for testing – visit /load_sample_data once."""
    conn = get_db()

    sample_production = [
        ('2024-11-01', 'Bracket A', 120),
        ('2024-11-05', 'Washer B',  300),
        ('2024-11-10', 'Pin C',     200),
        ('2024-11-15', 'Bracket A', 150),
        ('2024-12-01', 'Washer B',  400),
        ('2024-12-05', 'Clamp D',   180),
        ('2024-12-10', 'Pin C',     250),
        ('2025-01-03', 'Bracket A', 100),
        ('2025-01-08', 'Clamp D',   220),
        ('2025-01-12', 'Washer B',  350),
    ]

    sample_sales = [
        ('2024-11-03', 'Rajesh Industries',  'Bracket A', 50,  12.0),
        ('2024-11-07', 'Kumar Auto Parts',   'Washer B',  100,  5.5),
        ('2024-11-12', 'Venkatesan & Co',    'Pin C',      80,  8.0),
        ('2024-11-20', 'Rajesh Industries',  'Bracket A',  70, 12.0),
        ('2024-12-03', 'Global Fasteners',   'Washer B',  200,  5.5),
        ('2024-12-08', 'Kumar Auto Parts',   'Clamp D',    60, 18.0),
        ('2024-12-15', 'Venkatesan & Co',    'Pin C',     100,  8.0),
        ('2025-01-05', 'Global Fasteners',   'Bracket A',  90, 13.0),
        ('2025-01-09', 'Rajesh Industries',  'Clamp D',    50, 18.0),
        ('2025-01-14', 'Kumar Auto Parts',   'Washer B',  150,  6.0),
    ]

    sample_steel = [
        ('2024-10-28', 'Tata Steel Coimbatore', 500, 45000),
        ('2024-11-25', 'JSW Steel Chennai',      400, 37000),
        ('2024-12-20', 'Tata Steel Coimbatore',  600, 54000),
        ('2025-01-10', 'SAIL Distributor',        300, 27500),
    ]

    for row in sample_production:
        conn.execute('INSERT INTO production (date, product, pieces) VALUES (?,?,?)', row)

    for row in sample_sales:
        qty, price = row[3], row[4]
        conn.execute(
            'INSERT INTO sales (date, customer, product, quantity, price_per_pc, total_amount) VALUES (?,?,?,?,?,?)',
            (*row, qty * price)
        )

    for row in sample_steel:
        conn.execute('INSERT INTO steel_purchases (date, supplier, quantity_kg, cost) VALUES (?,?,?,?)', row)

    conn.commit()
    conn.close()
    flash('Sample data loaded successfully! Check the Dashboard.', 'success')
    return redirect(url_for('dashboard'))


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────

if __name__ == '__main__':
    init_db()  # Create tables on first run
    app.run(debug=True)
