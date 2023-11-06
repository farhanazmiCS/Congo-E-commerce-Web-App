from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import create, read, update, delete
from mongodbcontrollerV2 import MongoDBController

mongoController = MongoDBController()

ORDERS_PER_PAGE = 10

def get_all_orders(status_filter=None, skip=0, limit=ORDERS_PER_PAGE) -> list:
    query = []

    if status_filter:
        query.append({"$match": {"status": status_filter.lower()}})

    query.extend([
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
    ])

    return list(mongoController.aggregate('Orders', query))

@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', None)

    orders = get_all_orders(status_filter=status_filter, skip=(page-1)*ORDERS_PER_PAGE, limit=ORDERS_PER_PAGE)

    # Adjust the count_documents call based on the filter
    if status_filter:
        total_orders = mongoController.count_documents('Orders', {'status': status_filter})
    else:
        total_orders = mongoController.count_documents('Orders')

    total_pages = -(-total_orders // ORDERS_PER_PAGE)
    # If the orders are smaller than the page size, then there is only one page
    if total_pages == 0:
        total_pages = 1
    print(total_pages)

    return render_template('admin_orders.html', orders=orders, page=page, total_pages=total_pages, current_status=status_filter)