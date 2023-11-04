from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import create, read, update, delete

def remove_products():
    pass

def top_sold_products():
    pass

def update_stock():
    pass

@app.route('/admin')
def dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/inventory')
def inventory():
    return render_template('admin_inventory.html')