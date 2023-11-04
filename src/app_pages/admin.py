from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import create, read, update, delete
from mongodbcontrollerV2 import MongoDBController

mongoController = MongoDBController()

def get_total_sales_revenue():
    query = [
    {
        '$group': {
            '_id': 'null',
            'totalRevenue': { '$sum': '$total' }
        }
    }
]
    return list(mongoController.aggregate('Orders', query))

@app.route('/admin')
def dashboard():
    revenue = get_total_sales_revenue()
    return render_template('admin_dashboard.html', revenue=revenue)

@app.route('/admin/inventory')
def inventory():
    return render_template('admin_inventory.html')