import random
from __main__ import app
from ricefield import create, read, update, delete, mgdb
from flask import Flask, redirect, request, render_template, session, url_for

def get_random_image(category_id):
    # Fetch a random image associated with the given category_id from the products table
    product_image = read.select(
        columns=['productimg'],
        table='product',
        joins=[{'type': 'INNER', 'table': 'subcategory', 'condition': 'product.subcategoryid = subcategory.subcategoryid'},
               {'type': 'INNER', 'table': 'category', 'condition': 'subcategory.categoryid = category.categoryid'}],
        where=[f'category.categoryid = {category_id}'],
        orderBy={'RANDOM()': 'LIMIT 1'}
    )
    return product_image[0][0] if product_image else None

# Grab Top Sellers
def get_top_seller():
    pipeline = [
        {
            '$unwind': '$products'
        },
        {
            '$group': {
                '_id': '$products.product_id',
                'total': { '$sum': "$products.quantity" }
            }
        },
        {
            '$sort': { 'total': -1 }
        },
        {
            '$limit': 4
        }
    ]
    
    top_seller_list = list(mgdb.aggregate('Orders', pipeline))
    top_product = []

    for product in top_seller_list:
        productid = product['_id']
        quantitysold = product['total']

        product_from_db = read.select(
            table='product',
            where=[f'productid = {productid}'],
            )
        
        product_dict = {
            'product_id': product_from_db[0][0],
            'product_name': product_from_db[0][1],
            'product_image': product_from_db[0][3],
            'product_price': product_from_db[0][4],
            'product_rating': "N/A" if product_from_db[0][8] == 0.00 else product_from_db[0][8],
            'quantity_sold': quantitysold
        }

        top_product.append(product_dict)
    
    return top_product
        
# Grab Random Under $25
def get_under_25():
    product_under_25 = []

    products_from_db = read.select(
        table='product',
        where=["productprice < 25"],
        orderBy={'RANDOM()': 'LIMIT 4'}
    )
    
    for product in products_from_db:   
        product_dict = {
            'product_id': product[0],
            'product_name': product[1],
            'product_image': product[3],
            'product_price': product[4],
            'product_rating': "N/A" if product[8] == 0.00 else product[8]
        }
        product_under_25.append(product_dict)
        
    return product_under_25

@app.route('/',methods=['GET','POST'])
def homepage():
    # Number of categories to display per page
    items_per_page = 12

    # Fetch all categories from your database
    all_categories = read.select(
        columns=['categoryid', 'categoryname'],
        table='category',
        orderBy={'categoryname': 'ASC'}
    )

    # Randomly select 12 unique categories
    random_categories = random.sample(all_categories, items_per_page)

    # Fetch a random image for each of the randomly selected categories
    category_data = []
    for category in random_categories:
        category_id = category[0]
        image = get_random_image(category_id)
        category_data.append({"id": category_id, "name": category[1], "image": image})

    top_product = get_top_seller()
    product_under_25 = get_under_25()

    # Return the category_data to display on index.html
    return render_template('index.html', category_data=category_data,
                           top_product = top_product, product_under_25 = product_under_25)