import math
from __main__ import app
from ricefield import create, read, update, delete
from flask import Flask, flash, redirect, request, render_template, session, url_for
from .cart import getCart, getProducts, getProductDetails, removeProductFromCart, updateProductQuantity, saveSessionCarttoDB, updateProductInSessionCart

def get_product_details(product_id):
    product_details = read.select(
        table='product',
        where=[f'productid = {product_id}']
    )

    if product_details:
        product = product_details[0]
        
        # Get subcategory name
        subcategory_id = product[7]
        subcategory = read.select(
            table='subcategory',
            where=[f'subcategoryid = {subcategory_id}']
        )
        subcategoryname = subcategory[0][2] if subcategory else None
        
        # Get category ID
        category_id = subcategory[0][1] if subcategory else None
        
        # Get category name
        category = read.select(
            table='category',
            where=[f'categoryid = {category_id}']
        )
        categoryname = category[0][1] if category else None
        
        # Get supplier name
        supplier_id = product[6]
        supplier = read.select(
            table='supplier',
            where=[f'supplierid = {supplier_id}']
        )
        suppliername = supplier[0][1] if supplier else None
        
        product_dict = {
            'product_id': product[0],
            'product_name': product[1],
            'product_description': product[2],
            'product_image': product[3],
            'product_price': product[4],
            'product_stock': product[5],
            'subcategory_id': subcategory_id,
            'subcategory_name': subcategoryname,
            'category_id': category_id,
            'category_name': categoryname,
            'supplier_id': supplier_id,
            'supplier_name': suppliername
        }
        return product_dict
    else:
        return None  # Return None if the product is not found


@app.route('/product', methods=["GET", "POST"])
def product():
    product_id = request.args.get('id', type=int)
    if product_id is not None:
        product_details = get_product_details(product_id)
        if product_details:

            # Return product details
            return render_template('product.html', product=product_details)
        
@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    if 'user_id' not in session:
        session['error_message'] = "You must be logged in to add items to your cart"
        return redirect(url_for('login'))
    
    cart = session.get('cart') # Get the user's cart from the user's session

    product_id = request.form.get('product_id', type=int) # Get the product ID from the form
    product_name = request.form.get('product_name', type=str) # Get the product name from the form
    product_image = request.form.get('product_image', type=str) # Get the product image from the form
    product_quantity = request.form.get('product_quantity', type=int) # Get the quantity from the form
    product_price = request.form.get('product_price', type=float) # Get the price from the form
    product_stock = request.form.get('product_stock', type=int) # Get the stock from the form

    
    if product_id is not None and product_quantity is not None:
        for product in cart:
            if product.get('product_id') == product_id:
                # If the product is already in the cart, update the quantity
                product['product_price'] = product_price # setting the product price to the price of the product in the database (most recent)
                product['product_quantity'] += product_quantity
                updateProductInSessionCart(product_id)

                print(cart)
                print(product_price)
                saveSessionCarttoDB()
                return redirect(url_for('cart'))
                   
        else:
            # If the product is not in the cart, add it
            print(product_price)
            cart.append({
                'product_id': product_id,
                'product_name': product_name,
                'product_image': product_image,
                'product_price': product_price,
                'product_stock': product_stock,
                'product_quantity': product_quantity
            })
            print(cart)
            session['cart'] = cart # Update the user's session cart
            saveSessionCarttoDB() # Save the user's session cart to the database
       
            return redirect(url_for('cart'))
    return redirect(url_for('homepage'))

@app.route('/remove_from_cart', methods=["POST"])
def remove_from_cart():
    if 'user_id' not in session:
        session['error_message'] = "You must be logged in to remove items from your cart"
        return redirect(url_for('login'))
    removeProductFromCart(request.form.get('product_id', type=int))
    saveSessionCarttoDB()
    return redirect(url_for('cart'))