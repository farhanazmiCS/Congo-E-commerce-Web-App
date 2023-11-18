from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for,jsonify
from congoDB import create, read, update, delete
from congoDB import mgdb
from math import ceil

# Route to render the update categories and subcategories page
@app.route('/admin/category', methods=['GET'])
def admin_category():
    categories = []
    subcategories = []

    query = read.select(
        'category',
        orderBy={'categoryid': 'ASC'}
    )

    for result in query:
        category = {
            'categoryid': result[0],
            'categoryname': result[1],
            'categorydesc': result[2]
        }
        categories.append(category)

    query = read.select(
        'subcategory',
        orderBy={'subcategoryid': 'ASC'},
        joins = [{'type': 'INNER', 'table': 'category', 'condition': 'subcategory.categoryid = category.categoryid'}]
    )

    for result in query:
        subcategory = {
            'subcategoryid': result[0],
            'categoryid': result[1],
            'subcategoryname': result[2],
            'subcategorydesc': result[3],
            'maincategoryname': result[5]
        }
        subcategories.append(subcategory)

    return render_template('admin_categories.html', categories=categories, subcategories=subcategories)


# Route to update a category
@app.route('/update-category', methods=['POST'])
def update_category():
    category_id = request.form.get('category_id')
    category_name = request.form.get('category_name')
    category_description = request.form.get('category_description')

    # Perform the category update in the database
    update_query = update.update(
        table='category', 
        colvalues={
            'categoryname': category_name,
            'categorydescription': category_description
        },
        where=[f"categoryid='{category_id}'"]
    )
    return redirect('/admin/category')

# Route to update a subcategory
@app.route('/update-subcategory', methods=['POST'])
def update_subcategory():
    subcategory_id = request.form.get('subcategory_id')
    subcategory_name = request.form.get('subcategory_name')
    subcategory_description = request.form.get('subcategory_description')
    subcategory_category_id = request.form.get('subcategory_category_id')

    # Perform the subcategory update in the database
    update_query = update.update(
        table='subcategory', 
        colvalues={
            'subcategoryname': subcategory_name,
            'subcategorydescription': subcategory_description,
            'categoryid': subcategory_category_id
        },
        where=[f"subcategoryid='{subcategory_id}'"]
    )
    return redirect('/admin/category')