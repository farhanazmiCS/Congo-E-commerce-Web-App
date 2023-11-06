from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import create, read, update, delete
from mongodbcontrollerV2 import MongoDBController

mongoController = MongoDBController()

def get_all_orders() -> list:
    return list(mongoController.read('Orders'))


@app.route('/admin/orders', methods=['GET', 'POST'])
def admin_orders():
    print(get_all_orders())
    return render_template('admin_orders.html')