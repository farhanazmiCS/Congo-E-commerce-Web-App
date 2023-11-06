import math
from __main__ import app
from ricefield import create, read, update, delete
from flask import Flask, redirect, request, render_template, session, url_for
from .product import fetch_average_rating

def fetch_products(productname, page, category=None, max_price=None):
    products_per_page = 12
    offset = (page - 1) * products_per_page
    where_conditions = [f'productname ~* \'\\m{productname}\\M\'']

    if category is not None:
        where_conditions.append(f'categoryid = {category}')
    
    if max_price is not None:
        where_conditions.append(f'productprice <= {max_price}')
    
    where_clause = ' AND '.join(where_conditions)

    products = read.select(
        table='product',
        where=[where_clause],
        joins=[{'type': 'INNER', 'table': 'subcategory', 'condition': 'product.subcategoryid = subcategory.subcategoryid'}],
        orderBy={'productname': 'ASC'},
        limit=products_per_page,
        offset=offset
    )

    print(products)
    product_list = []

    for product in products:
        averageRating = fetch_average_rating(product[0])

        product_dict = {
            'product_id': product[0],
            'product_name': product[1],
            'product_image': product[3],
            'product_price': product[4],
            'product_rating': averageRating
        }

        product_list.append(product_dict)
    
    return product_list

def get_total_products(productname, category=None, max_price=None):
    products_per_page = 12

    where_conditions = [f'productname ~* \'\\m{productname}\\M\'']

    if category is not None:
        where_conditions.append(f'categoryid = {category}')
    
    if max_price is not None:
        where_conditions.append(f'productprice <= {max_price}')
    
    where_clause = ' AND '.join(where_conditions)

    products = read.select(
        columns=['COUNT(*)'],
        where=[where_clause],
        table='product',
        joins=[{'type': 'INNER', 'table': 'subcategory', 'condition': 'product.subcategoryid = subcategory.subcategoryid'}])
    total_pages = math.ceil((products[0][0])/products_per_page)
    
    return total_pages

def get_categories():
    categories = read.select(
        columns=['categoryid', 'categoryname'],
        table='category'
    )
    return categories

@app.route('/search-result', methods=["GET"])
def searchResult():
    productname = request.args.get('productname', default='NULL', type=str)
    page = request.args.get('page', default=1, type=int)
    category = request.args.get('filter_category', default=None, type=int)
    max_price = request.args.get('filter_price', default=None, type=float)

    total_pages = get_total_products(productname, category, max_price)
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    # Get Product Name with filters
    products = fetch_products(productname, page, category, max_price)

    # Get categories for the dropdown
    categories = get_categories()

    return render_template('search-result.html', searchTerm=productname, products=products,
                           page=page, total_pages=total_pages,
                           start_page=start_page, end_page=end_page,
                           categories=categories, selected_category=category,
                           max_price=max_price)