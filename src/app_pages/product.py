import math
from __main__ import app
from ricefield import create, read, update, delete
from flask import Flask, redirect, request, render_template, session, url_for

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

        print(product_details)
        if product_details:


            # Return product details
            return render_template('product.html', product=product_details)