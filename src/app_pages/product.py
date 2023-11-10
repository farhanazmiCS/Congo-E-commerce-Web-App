from datetime import datetime
import math
from __main__ import app
from ricefield import create, read, update, delete, mgdb
from flask import Flask, flash, redirect, request, render_template, session, url_for
from .cart import getCart, getProducts, getProductDetails, removeProductFromCart, updateProductQuantity, saveSessionCarttoDB, updateProductInSessionCart

def fetch_user_reviews(product_id, page=1, reviews_per_page=5):
    skip_count = (page - 1) * reviews_per_page
    
    pipeline = [
        {
            '$match': {
                'productID': product_id
            }
        },
        {
            '$unwind': '$reviews'
        },
        {
            '$sort': {
                'reviews.timestamp': -1  # Sort reviews by timestamp in descending order (latest first)
            }
        },
        {
            '$group': {
                '_id': '$productID',
                'reviews': {
                    '$push': '$reviews'
                }
            }
        }
    ]

    result = list(mgdb.aggregate('Reviews', pipeline))

    if result:
        reviews = result[0].get('reviews', [])
        total_reviews = len(reviews)

        # Calculate the total number of pages
        total_pages = math.ceil(total_reviews / reviews_per_page)

        # Calculate the start and end indices for reviews on the current page
        start_index = skip_count
        end_index = min(start_index + reviews_per_page, total_reviews)

        # Slice the reviews to get the ones for the current page
        reviews_on_page = reviews[start_index:end_index]

        return reviews_on_page, total_pages
    else:
        return [], 0  # Return an empty list and 0 pages if no reviews found

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
        suppliercontact = supplier[0][2] if supplier else None
        
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
            'supplier_name': suppliername,
            'supplier_contact': suppliercontact,
            'product_rating': "N/A" if product[8] == 0.00 else product[8]
        }
        return product_dict
    else:
        return None  # Return None if the product is not found


@app.route('/product', methods=["GET", "POST"])
def product():

    product_id = request.args.get('id', type=int)
    page = request.args.get('page', type=int, default=1)

    if product_id is not None:
        product_details = get_product_details(product_id)
        if product_details:

            # Fetch user reviews and calculate total pages
            user_reviews, total_pages = fetch_user_reviews(product_id, page=page)

            # Return product details
            return render_template('product.html', product=product_details, user_reviews=user_reviews,
                                   total_pages=total_pages, current_page=page)

def calculate_average_rating(product_id):
    # Aggregate the reviews to calculate the average rating
    pipeline = [
        { # Selects the documents where the value of the 'productID' field equals 'product_id'
            '$match': {
                'productID': product_id  
            }
        },
        { # Deconstructs the 'reviews' array field from the input documents to output a document for each element
            '$unwind': '$reviews'  
        },
        {
            '$group': { # Groups the input documents by the specified '_id' expression
                '_id': '$productID',  
                'averageRating': { # Computes the average 'rating' for each distinct group
                    '$avg': '$reviews.rating'  
                }
            }
        }
    ]

    result = list(mgdb.aggregate('Reviews', pipeline))

    if result:
        # Extract the average rating from the result
        average_rating = result[0].get('averageRating')

        # Update the product's average rating in SQL DB
        query = update.update(
        table='product',
        colvalues={'productrating': round(average_rating,2)},
        where=[f'productid = {product_id}'])


@app.route('/review', methods=["POST"])
def review():
    if request.method == "POST":
        # Get review data from the form
        product_id = request.form.get('product_id', type=int)
        rating = request.form.get('rating', type=int)
        review = request.form.get('review', type=str)
        user_id = session.get('user_id')
        user_name = session.get('user_name')

        # Prepare the review data
        review_data = {
            'userid': user_id,
            'name': user_name,
            'rating': rating,
            'review': review,
            'timestamp': datetime.now()
        }
        # Find the existing record for the product in the reviews collection
        existing_review = list(mgdb.read('Reviews', {'productID': product_id}))
        
        print(existing_review)

        if len(existing_review) > 0:
            # If the record already exists, append the new review to the 'reviews' field
            existing_review_data = existing_review[0]
            reviews_list = existing_review_data.get('reviews', [])
            reviews_list.append(review_data)
            
            # Update the reviews field with the new review data
            mgdb.update('Reviews', {'productID': product_id}, {'reviews': reviews_list})
        else:
            # If the record doesn't exist, create a new one with the 'reviews' field
            mgdb.create('Reviews', {'productID': product_id, 'reviews': [review_data]})

        # Calculate the average rating for the product
        calculate_average_rating(product_id)

        # Redirect to the product page with the anchor fragment
        return redirect(url_for('product') + '?id=' + str(product_id) + '#review')

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