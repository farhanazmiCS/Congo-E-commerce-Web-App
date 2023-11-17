from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from congoDB import read, create, update, delete
from controller.mongodbController import MongoDBController


# Returns the cart of the user as a list
# If the user does not have a cart, returns None
# If the user is not logged in, redirects to login page
def getCart():
    if 'user_id' in session:
        controller = MongoDBController()
        cart_cursor = controller.read('Cart', {'user_id': session['user_id']})
        cart = list(cart_cursor)  # Convert the cursor to a list of documents
        if cart:
            return cart[0]
    else:
        session['error_message'] = "You must be logged in to view your cart"
        return redirect(url_for('login'))

# Returns the products in the cart as an array of product dictionaries
# If the cart is empty, returns None
def getProducts(cart):
    if cart is not None:
        product_array = []  # Array of product dictionaries
        # getting total products in cart
        products = cart.get('products', [])
        for product in products:  # looping through each product in cart
            # getting product id to perform details query
            product_id = product.get('product_id')
            product_details = getProductDetails(
                product_id, product.get('product_quantity'))  # getting product details

            if product_details is not None:  # if the product exist and is in stock
                # product_details['product_quantity'] = product.get('quantity') # adding quantity to product details
                # adding product details to array
                product_array.append(product_details)
        return product_array

def updateProductInSessionCart(product): # updates a product in the session cart with new price and quantity
    cart = session['cart']
    for product in cart:
        if product.get('product_id') == product.get('product_id'):
            product['product_quantity'] = product['product_quantity']
            product['product_price'] = product['product_price']
            break
    session['cart'] = cart

# removes a product from the session cart
def removeProductFromCart(product_id):
    cart = session['cart']
    for product in cart:
        if product.get('product_id') == product_id:
            cart.remove(product)
            break
    session['cart'] = cart

def updateProductQuantity(product_id, product_quantity):
    cart = session['cart']
    for product in cart:
        if product.get('product_id') == product_id:
            product['product_quantity'] = product_quantity
            break
    session['cart'] = cart

def ConvertToDbCart(cart):
    db_cart = []
    for product in cart:
        db_cart.append({'product_id': product.get('product_id'), 'product_quantity': product.get('product_quantity')})
    return db_cart

# saves the session cart to the MongoDB
def saveSessionCarttoDB():
    controller = MongoDBController()
    cart = session['cart']
    db_cart = ConvertToDbCart(cart)
    # get only product id and quantity from session cart
    
    controller.update('Cart', {'user_id': session['user_id']}, {'products': db_cart})

# gets product details from SQL
def getProductDetails(product_id, product_quantity):
    product = read.select(
        table='product',
        columns=['productid', 'productname',
                 'productimg', 'productprice', 'productstock'],
        where=[f'productid = {product_id}']
    )

    if not product:  # if product does not exist
        removeProductFromCart(product_id) # remove invalid product from session cart
        saveSessionCarttoDB() # save session cart to database
        return None  # no error message for this. Just silently exclude it

    product_stock = product[0][4]
    product_name = product[0][1]

    if product_stock == 0: # if product is out of stock
        removeProductFromCart(product_id) # remove product from session cart
        saveSessionCarttoDB() # save session cart to database
        session['error_message'].append(
            f"Product {product_name} has been removed from your cart as it is out of stock, ")
        return None
    
    elif product_stock < product_quantity: # if product stock is less than quantity in cart
        product_quantity = product_stock # set quantity to available stock
        updateProductQuantity(product_id, product_quantity) # update quantity in session cart
        saveSessionCarttoDB() # save session cart to database
        session['error_message'].append(
            f"Product {product_name} has less stock than the quantity in your cart. Quantity has been reduced to available stock, ")
        product_quantity = product_stock

    if product:
        product_details = {
            'product_id': product[0][0],
            'product_name': product[0][1],
            'product_image': product[0][2],
            # convert product price to Float in 2 decimal places
            'product_price': "{:.2f}".format(float(product[0][3])),
            'product_stock': product[0][4],
            'product_quantity': product_quantity
        }
        return product_details

def getSubtotal(products):
    subtotal = 0
    for product in products:
        print(product)
        subtotal += float(product.get('product_price')) * \
            int(product.get('product_quantity'))
    # return subtotal to 0.2f as float
    return "{:.2f}".format(subtotal)

@app.route('/cart', methods=["GET", "POST"])
def cart():
    # Initialize an error message variable
    session.setdefault('error_message', [])
    if session.get('user_id') is None:
        session['error_message'] = "You must be logged in to view your cart"
        return redirect(url_for('login'))

    # print("the user id is: ")
    # print(session.get('user_id'))
    # print(session.get('cart'))
    # if the session cart is empty, pull cart from database
    if not session.get('cart') or session.get('cart') == []:
        cart = getCart()
        products = getProducts(cart)
        session['cart'] = products
        subtotal = getSubtotal(products)

    else:  # if the session cart is not empty, use the session cart
        # print("session cart not empty")
        # print(session.get('cart'))
        products = session['cart']
        subtotal = getSubtotal(products)

    # session['error_message'].append("Banana, ")
    # session['error_message'].append("Apple, ")
    # session['error_message'].append("Orange, ")

    return render_template('cart.html', products=products, subtotal=subtotal)
