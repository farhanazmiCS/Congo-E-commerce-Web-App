import random
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

    # Return the category_data to display on index.html
    return render_template('index.html', category_data=category_data)