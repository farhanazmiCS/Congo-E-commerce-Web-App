import math
from __main__ import app
from ricefield import create, read, update, delete
from flask import Flask, redirect, request, render_template, session, url_for
from PostGresControllerV2.PostGresControllerV2 import initialise_crud


def fetch_products(productname, page):
    products_per_page = 12
    offset = (page - 1) * products_per_page
    products = read.select(
        table='product',
        where=[f'productname LIKE \'%{productname}%\' ORDER BY productid ASC LIMIT {products_per_page} OFFSET {offset}'])
    return products

def get_total_products(productname):
    products_per_page = 12
    products = read.select(
        columns=['COUNT(*)'],
        table='product',
        where= [f'productname LIKE \'%{productname}%\''])
    total_pages = math.ceil((products[0][0])/products_per_page)
    
    return total_pages

@app.route('/search-result', methods=["GET"])
def searchResult():
    productname = request.args.get('productname', default='NULL', type=str)
    page = request.args.get('page', default=1, type=int)
    
    total_pages = get_total_products(productname)
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    # Get Product Name
    products = fetch_products(productname, page)

    return render_template('search-result.html', searchTerm=productname, products=products,
                           page=page, total_pages=total_pages, 
                           start_page=start_page, end_page=end_page)