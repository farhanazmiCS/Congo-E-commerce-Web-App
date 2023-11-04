from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import read, create, update, delete
from mongodbcontrollerV2 import MongoDBController
import numpy as np
import plotly.express as px
import pandas as pd
from app_pages.cart import getProducts, getSubtotal
from app_pages.orders import getOrders
from app_pages.category import get_category_name

mgdb = MongoDBController()

#get orders belonging to the user and return it as a list 
def getSortedOrders(field,order):
     if 'user_id' in session:
        print('notfailed')
        orderData = mgdb.read("Orders",{ "user_id": session['user_id'] })
        orderList=list(orderData)
        orderList = sorted(orderList, key=lambda d: d[field], reverse=order)
        return orderList
     
#get orders belonging to the user and return it as a list 
def getShippedOrders():
     if 'user_id' in session:
        print('notfailed')
        orderData = mgdb.read("Orders",{ "$and" : [{"user_id": session['user_id'] },{"status": "shipped" }]})
        print(orderData)
        orderList=list(orderData)
        for order in orderList:
            print(order['status'])
        return orderList
     
def getProductQuantity(orderList):
    productQuantityDict={}
    for order in orderList:
        for product in order['products']:
            if product['product_id'] in productQuantityDict.keys():
                productQuantityDict[product['product_id']][1] += product['product_quantity']
            else:
                productQuantityDict[product['product_id']] = [product['product_name'],product['product_quantity'],product['product_price']]

    print( productQuantityDict)
    sortedProductQuantityList = sorted(productQuantityDict.items(), key=lambda x:x[1][1], reverse=True)
    print( sortedProductQuantityList)
    return  sortedProductQuantityList

def getTotalExpenditure(orderList):
    totalExpenditure=0
    for order in orderList:
        totalExpenditure += order['total']

    return totalExpenditure


def getTotalQuantity(sortedProductQuantityList):
    totalQuantity = 0
    for product in sortedProductQuantityList:
        totalQuantity += product[1][1]

    return totalQuantity

#get orders belonging to the user and return it as a list 
def getOrdersNeedingPayment():
     if 'user_id' in session:
        print('notfailed')
        orderData = mgdb.read("Orders",{ "$and" : [{"user_id": session['user_id'] },{"status": "awaiting payment" }]})
        print(orderData)
        orderList=list(orderData)
        for order in orderList:
            print(order['status'])
        return orderList
     
def mostExpensiveOrder(orderList):
    max=0
    for order in orderList:
        if order['total']>max:
            max=order['total']

    return max






@app.route('/user_dashboard', methods=["GET", "POST"])
def userDashboard():
    # Initialize an error message variable
    session.setdefault('error_message', [])
    
    if session.get('user_id') is None:
        session['error_message'] = "You must be logged in to view your cart"
        return redirect(url_for('login'))
    print('notfailed0')
    orderList = getOrders()
    print(orderList)
    recentOrderList = getSortedOrders("total", True)[:5]
    shippedOrderList = getShippedOrders()[:5]
    sortedProductQuantityList = getProductQuantity(orderList)[:5]
    totalExpenditure = getTotalExpenditure(orderList)
    totalQuantity = getTotalQuantity(sortedProductQuantityList)
    print(sortedProductQuantityList)
    maxTotal=mostExpensiveOrder(orderList)
    ordersNeedingPayment=getOrdersNeedingPayment()

    return render_template('user_dashboard.html', recentOrderList = recentOrderList , shippedOrderList = shippedOrderList, sortedProductQuantityList = sortedProductQuantityList, totalExpenditure = totalExpenditure , totalQuantity = totalQuantity,ordersNeedingPayment = ordersNeedingPayment,maxTotal=maxTotal)