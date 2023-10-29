from __main__ import app
from bson import ObjectId
from flask import Flask, redirect, request, render_template, session, url_for
from mongodbcontrollerV2 import MongoDBController
from app_pages.cart import getCart, getProducts, getSubtotal
import datetime

mgdb = MongoDBController()


def checkout(cart: dict, order_total: float):
    # if cart['products'] == []:
    #     print("Cart is empty")  
    #     return redirect(url_for('cart'))
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    arrival_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%d/%m/%Y")
    data = {
        'user_id': cart['user_id'],
        'products': cart['products'],
        'date': date,
        'status': 'pending',
        'arrival_date': arrival_date,
        'total': order_total
    }
    _id = mgdb.create('Orders', data)
    mgdb.update('Cart', {'user_id': cart['user_id']}, {'products': []})
    #!!! REMEMBER TO IMPLEMENT THE UPDATE OF THE PRODUCT STOCK
    
    return _id.inserted_id

   


def getOrderDetail(id: int):
    query = {"_id": ObjectId(id)}
    return list(mgdb.read('Orders', query))


@app.route('/order', methods=["GET", "POST"])
def order():
    cart = getCart()
    products = getProducts(cart)
    ordertotal = getSubtotal(products)
    order_id = checkout(cart, ordertotal)
    print(order_id)
    order_detail = getOrderDetail(order_id)
    print(order_detail)
    

    return render_template('order.html', order_detail=order_detail, ordertotal=ordertotal, products=products)
