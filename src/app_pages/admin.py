from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import create, read, update, delete
from mongodbcontrollerV2 import MongoDBController

mongoController = MongoDBController()

def get_total_sales_revenue() -> list:
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

def get_total_sales_revenue_by_month_and_year(month: int, year: int) -> list:
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

def get_best_selling_product() -> list:
    """
        Notes:
            The "$unwind" keyword "unpacks" an array of objects. For example, 
            the Orders collection feature the "products" attribute, which contain
            a list of products. The $unwind keyword is used to "duplicate" the records.
            Let's say an order contain 3 products. As such, instead of having the three
            products in one order, the three products would be separated into three
            SEPARATE orders.

            $first is an aggregation keyword used for getting the "first" value of the group's
            instance. For example, now we have multiple orders (from the $unwind action). As such,
            we would like the $product_name, $product_image, etc. to follow the first object.

    """
    query = [
        { '$unwind': "$products" },
        {
            '$group': {
                '_id': "$products.product_id",
                'product_name': { '$first': "$products.product_name" },
                'product_image': { '$first': "$products.product_image" },
                'product_price': { '$first': "$products.product_price" },
                'product_stock': { '$first': "$products.product_stock" },
                'totalQuantity': { '$sum': "$products.product_quantity" }
            }
        },
        { '$sort': { 'totalQuantity': -1 } },
        { '$limit': 1 },
        {
            '$project': {
                '_id': 0,
                'product_id': "$_id",
                'product_name': 1,
                'product_image': 1,
                'product_price': 1,
                'product_stock': 1,
                'totalQuantity': 1
            }
        }
    ]
    return list(mongoController.aggregate('Orders', query))


@app.route('/admin')
def dashboard():
    revenue = get_total_sales_revenue()
    revenue_month_year = get_total_sales_revenue_by_month_and_year(1, 2023)
    best_selling_product = get_best_selling_product()
    return render_template('admin_dashboard.html', revenue=revenue, revenue_month_year=revenue_month_year, best_selling_product=best_selling_product)

@app.route('/admin/inventory')
def inventory():
    return render_template('admin_inventory.html')