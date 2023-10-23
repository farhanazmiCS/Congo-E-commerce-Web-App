import math
from __main__ import app
from ricefield import create, read, update, delete
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

@app.route('/categories', methods=["GET","POST"])
def categories():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 12  # Number of categories to display per page

    # Fetch all categories from your database
    categories = read.select(
        columns=['categoryid', 'categoryname'],
        table='category',
        orderBy={'categoryname': 'ASC'},
        limit=items_per_page,
        offset=(page - 1) * items_per_page
    )

    # Calculate the total number of categories
    total_categories = read.select(
        columns=['COUNT(*)'],
        table='category'
    )

    # Calculate the total number of pages
    total_pages = math.ceil(total_categories[0][0] / items_per_page)

    # Fetch a random image for each category from the subcategories table
    category_data = []
    for category in categories:
        category_id = category[0]
        image = get_random_image(category_id)
        category_data.append({"id": category_id, "name": category[1], "image": image})

    return render_template('categories.html', categories=category_data, page=page, total_pages=total_pages)
