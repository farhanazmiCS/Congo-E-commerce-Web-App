from __main__ import app
from bson import ObjectId
from ricefield import create, read, update, delete
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

    products_to_checkout = []

    # Fix for Misisng Product Details
    for cart_product in cart['products']:
        product_id = cart_product['product_id']
        quantity = cart_product['product_quantity']
        product_info = read.select(table='product', where=[f"productid = '{product_id}'"])

        print(product_info)

        product_name = product_info[0][1]
        product_image = product_info[0][3]
        product_price = float(product_info[0][4])

        products_to_checkout.append({'product_id': product_id,
                                    'product_name': product_name,
                                    'product_image': product_image,
                                    'product_price': product_price,
                                    'product_quantity': quantity})


    data = {
        'user_id': cart['user_id'],
        'products': products_to_checkout,
        'date': date,
        'status': 'pending',
        'arrival_date': arrival_date,
        'total': float(order_total)
    }
    _id = mgdb.create('Orders', data)
    mgdb.update('Cart', {'user_id': cart['user_id']}, {'products': []})
    #clear session cart
    session['cart'] = []
    #!!! REMEMBER TO IMPLEMENT THE UPDATE OF THE PRODUCT STOCK
    
    return _id.inserted_id

   


def getOrderDetail(id: int):
    query = {"_id": ObjectId(id)}
    return list(mgdb.read('Orders', query))


#delete an order   
def deleteOrderSingle(orderId:int):
   mgdb.delete("Orders",{ "_id": orderId })


@app.route('/order', methods=["GET", "POST"])
def order():
    # Initialize an error message variable
    session.setdefault('error_message', [])
    if session.get('user_id') is None:
        session['error_message'] = "You must be logged in to place an order"
        return redirect(url_for('login'))

    if request.method == "POST":
        cart = getCart()
        products = getProducts(cart)
        ordertotal = getSubtotal(products)
        print("CART: ", cart)
        order_id = checkout(cart, ordertotal)
        print(order_id)
        order_detail = getOrderDetail(order_id)
        print(order_detail)

        return render_template('order.html', order_detail=order_detail, ordertotal=ordertotal, products=products, order_id=order_id)
    else:
        # If it's not a POST request, redirect to the homepage
        return redirect(url_for('homepage'))

@app.route('/cancel_order', methods=["GET", "POST"])
def selectCancelOrder():
     # Initialize an error message variable
    session.setdefault('error_message', [])
    if session.get('user_id') is None:
        session['error_message'] = "You must be logged in to view your cart"
        return redirect(url_for('login'))
    session.setdefault('status_message', [])
    if request.method == 'GET' and request.args.get('order_id'):
        order_id= request.args.get('order_id')
        deleteOrderSingle(order_id)
        session['status_message'] = "Order Deleted."    
        return redirect(url_for('orders'))
    else:
        session['error_message'] = "Order does not exist."
        return redirect(url_for('orders'))
   