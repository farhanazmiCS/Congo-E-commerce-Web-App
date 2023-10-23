import math
from __main__ import app
from ricefield import create, read, update, delete
from flask import Flask, redirect, request, render_template, session, url_for

def get_random_image(subcategory_id):
    # Fetch a random image associated with the given subcategory_id from the products table
    product_image = read.select(
        columns=['productimg'],
        table='product',
        where=[f'subcategoryid = {subcategory_id}'],
        orderBy={'RANDOM()': 'LIMIT 1'}
    )
    return product_image[0][0] if product_image else None

@app.route('/subcategories', methods=["GET", "POST"])
def subcategories():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 24  # Number of subcategories to display per page

    # Fetch all subcategories from your database
    subcategories = read.select(
        columns=['subcategoryid', 'subcategoryname'],
        table='subcategory',
        orderBy={'subcategoryname': 'ASC'},
        limit=items_per_page,
        offset=(page - 1) * items_per_page
    )

    # Calculate the total number of subcategories
    total_subcategories = read.select(
        columns=['COUNT(*)'],
        table='subcategory'
    )

    # Calculate the total number of pages
    total_pages = math.ceil(total_subcategories[0][0] / items_per_page)

    # Fetch a random image for each subcategory from the product table
    subcategory_data = []
    for subcategory in subcategories:
        subcategory_id = subcategory[0]
        image = get_random_image(subcategory_id)
        subcategory_data.append({"id": subcategory_id, "name": subcategory[1], "image": image})

    return render_template('subcategories.html', subcategories=subcategory_data, page=page, total_pages=total_pages)
