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
        },
        {
            '$project': {
                '_id': 0,  # Exclude the _id field from the output
                'totalRevenue': {'$round': ['$totalRevenue', 2]}  # Round the total revenue to 2 decimal places
            }
        }
    ]
    return list(mongoController.aggregate('Orders', query))

def get_total_sales_revenue_by_month_and_year(month: int, year: int):
    month_year_str = f"{month}/{year}"
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    query = [
        {
            '$match': {
                'date': {
                    '$regex': f'^\\d{{2}}/{month_year_str}' # This regex matches any date that ends with the specified month/year
                }
            }
        },
        {
            '$group': {
                '_id': None, # Grouping by null means group all documents together
                'totalRevenue': { '$sum': '$total' } # Summing up all the 'total' fields
            }
        },
        {
            '$project': {
                '_id': 0,  # Exclude the _id field from the output
                'totalRevenue': {'$round': ['$totalRevenue', 2]}  # Round the total revenue to 2 decimal places
            }
        }
    ]
    aggr = list(mongoController.aggregate('Orders', query))
    aggr.append(months[month])
    return aggr

@app.route('/admin')
def dashboard():
    revenue = get_total_sales_revenue()
    revenue_month_year = get_total_sales_revenue_by_month_and_year(1, 2023)
    return render_template('admin_dashboard.html', revenue=revenue, revenue_month_year=revenue_month_year)

@app.route('/admin/inventory')
def inventory():
    return render_template('admin_inventory.html')