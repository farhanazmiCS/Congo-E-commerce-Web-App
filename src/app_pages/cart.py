from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import read, create, update, delete
from mongodbcontrollerV2 import MongoDBController


def getCart():
    if 'user_id' in session:
        controller = MongoDBController()
        cart_cursor = controller.read('Cart', {'user_id': session['user_id']})
        cart = list(cart_cursor)  # Convert the cursor to a list of documents
        for cart_item in cart:
            return cart_item  # normally, only 1 cart item in cart, as users can only have 1 cart
    else:
        error_message += "User not logged in or an error occurred, "
        return None


def getProducts(cart_item):
    if cart is not None:
        product_array = []  # Array of product dictionaries
        # getting total products in cart
        products = cart_item.get('products', [])
        for product in products:  # looping through each product in cart
            # getting product id to perform details query
            product_id = product.get('product_id')
            product_details = getProductDetails(
                   product_id, product.get('quantity'))  # getting product details

            if product_details is not None:  # if the product exist and is in stock
                    # product_details['product_quantity'] = product.get('quantity') # adding quantity to product details
                    # adding product details to array
                    product_array.append(product_details)
        return product_array


def getProductDetails(product_id, product_quantity):
    product = read.select(
        table='product',
        columns=['productid', 'productname',
                 'productimg', 'productprice', 'productstock'],
        where=[f'productid = {product_id}']
    )

    if not product:  # if product does not exist
        return None  # no error message for this. Just silently exclude it

    product_stock = product[0][4]
    product_name = product[0][1]

    if product_stock == 0:
        error_message += "Product {product_name} has been removed from your cart as it is out of stock, "
        return None
    elif product_stock < product_quantity:
        error_message += "Product {product_name} has less stock than the quantity in your cart. Quantity has been reduced to available stock, "
        product_quantity = product_stock

    if product:
        product_details = {
            'product_id': product[0][0],
            'product_name': product[0][1],
            'product_image': product[0][2],
            'product_price': product[0][3],
            'product_stock': product[0][4],
            'product_quantity': product_quantity
        }
        return product_details


def getSubtotal(products):
    subtotal = 0
    for product in products:
        subtotal += float(product.get('product_price')) * \
            int(product.get('product_quantity'))
    return subtotal


@app.route('/cart', methods=["GET", "POST"])
def cart():
    error_message = ""  # Initialize an error message variable
    # print(session.get('cart'))
    if session.get('user_id') is None:
        error_message += "User not logged in or an error occurred, "
        session['error_message'] = error_message
        return redirect(url_for('login'))
    
    #if the session cart is empty, pull cart from database
    if session.get('cart') == []:
        cart = getCart()
        products = getProducts(cart)
        print(products)
        session['cart'] = products
        subtotal = getSubtotal(products)
        print(session['cart'])

    else: #if the session cart is not empty, use the session cart
        products = session['cart']
        subtotal = getSubtotal(products)

    error_message += "Banana, "
    error_message += "Apple, "
    error_message += "Orange, "

    if error_message:  # Check if there are any error messages
        # Split the error messages by comma and space
        error_messages = error_message.split(", ")
        error_messages.pop()  # Remove the last element from the list as it is an empty string
    else:
        error_messages = []

    return render_template('cart.html', products=products, subtotal=subtotal, error_messages = error_messages)
