from __main__ import app
from bson import ObjectId
from flask import Flask, redirect, request, render_template, session, url_for ,jsonify, make_response
from controller.mongodbController import MongoDBController
import datetime
import json

mgdb = MongoDBController()


#get orders belonging to the user and return it as a list 
def getOrders():
     if 'user_id' in session:
        orderData = mgdb.read("Orders",{ "user_id": session['user_id'] })
        orderList=list(orderData)
        print(orderList)
        return orderList
     

#delete an order   
def deleteOrder(orderId:int):
    mgdb.delete("Orders",{ "_id": orderId })

#check status of an order and return it
def checkOrderStatus(orderId:int):
    order = mgdb.read("Orders",{ "_id": orderId })
    orderList = list(order)
    print(orderList[0]["status"])
    return orderList[0]["status"]

#set status of an order and return it
#not implemented yet
def setOrderStatus(orderId:int,status:str):
    order = mgdb.update("Orders",{ "_id": orderId },{"status":status})
    


@app.route('/orders', methods=["GET", "POST"])
def orders():
    # Initialize an error message variable
    session.setdefault('error_message', [])
    if session.get('user_id') is None:
        session['error_message'] = "You must be logged in to view your orders"
        return redirect(url_for('login'))
    
    orderList=getOrders()
    print(orderList)
    return render_template('orders.html', orders=orderList)



@app.route('/cancel_order_ajax', methods=["GET", "POST"])
def removeOrder():
    reqdata=request.get_json()
    cancelledOrder = reqdata['deletedOrderId']
    if checkOrderStatus(cancelledOrder) == 'pending':
        setOrderStatus(cancelledOrder,"cancelled")
        responseMessage="Order has been Cancelled."
        res=make_response(jsonify({ "response_message": responseMessage, "order_id": cancelledOrder}))
    else:
        responseMessage="Order cannot be been deleted because it is "+ checkOrderStatus(cancelledOrder) + "."
        res=make_response(jsonify({ "response_message": responseMessage,"order_id": -1}))
    
    
    return res
