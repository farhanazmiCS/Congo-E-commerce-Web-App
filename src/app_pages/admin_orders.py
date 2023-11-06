from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import create, read, update, delete
from mongodbcontrollerV2 import MongoDBController

mongoController = MongoDBController()

ORDERS_PER_PAGE = 10

def get_all_orders(skip=0, limit=ORDERS_PER_PAGE) -> list:
    orders = list(mongoController.aggregate('Orders', [
        {"$skip": skip},
        {"$limit": limit},
        {
            "$project": {
                "user_id": 1,
                "status": 1,
                "date": 1,
                "total": 1
            }
        }
    ]))
    return orders

@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    page = request.args.get('page', 1, type=int)
    skip = (page-1) * ORDERS_PER_PAGE
    limit = ORDERS_PER_PAGE
    
    # Adjust the query to fetch only a subset of orders
    orders = get_all_orders(skip, limit)
    
    total_orders = mongoController.count_documents('Orders')
    total_pages = -(-total_orders // ORDERS_PER_PAGE) 

    return render_template('admin_orders.html', orders=orders, page=page, total_pages=total_pages)