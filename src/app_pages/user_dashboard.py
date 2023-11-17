from __main__ import app
from flask import Flask, redirect, request, render_template, session, url_for
from ricefield import read, create, update, delete
from mongodbcontrollerV2 import MongoDBController
import numpy as np
import plotly.express as px
import pandas as pd
import datetime as datetime
from app_pages.orders import getOrders

mgdb = MongoDBController()

#get orders belonging to the user and return it as a list 
def getSortedOrdersByDate(dateType,order):
     if 'user_id' in session:
        orderData = mgdb.read("Orders",{ "user_id": session['user_id'] })
        orderList=list(orderData)
        orderList = sorted(orderList, key=lambda d: datetime.datetime.strptime(d[dateType], "%d/%m/%Y"), reverse=order)
        return orderList
     
#get orders belonging to the user and return it as a list 
def getSortedOrders(field,order):
     if 'user_id' in session:
        orderData = mgdb.read("Orders",{ "user_id": session['user_id'] })
        orderList=list(orderData)
        orderList = sorted(orderList, key=lambda d: d[field], reverse=order)
        return orderList
     
#get orders belonging to the user and return it as a list 
def getShippedOrders():
     if 'user_id' in session:
        orderData = mgdb.read("Orders",{ "$and" : [{"user_id": session['user_id'] },{"status": "shipped" }]})
        orderList=list(orderData)
        return orderList
     
def getProductQuantity(orderList):
    productQuantityDict={}
    for order in orderList:
        for product in order['products']:
            if product['product_id'] in productQuantityDict.keys():
                productQuantityDict[product['product_id']][1] += product['product_quantity']
            else:
                productQuantityDict[product['product_id']] = [product['product_name'],product['product_quantity'],product['product_price']]

    sortedProductQuantityList = sorted(productQuantityDict.items(), key=lambda x:x[1][1], reverse=True)
    return  sortedProductQuantityList

def getTotalExpenditure(orderList):
    totalExpenditure = 0
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
        orderData = mgdb.read("Orders",{ "$and" : [{"user_id": session['user_id'] },{"status": "awaiting payment" }]})
        print(orderData)
        orderList=list(orderData)
        return orderList
     
def mostExpensiveOrder(orderList):
    max=0
    for order in orderList:
        if order['total']>max:
            max=order['total']

    return max

def listOfExpenditureByMonth(sortedOrderList):
    orderDict={}
    orderNoDict={}
    for order in sortedOrderList:
        dateObj = datetime.datetime.strptime(order['date'],'%d/%m/%Y')
        monthYear = str(dateObj.month) + '/' + str(dateObj.year)
        print(monthYear)
        if monthYear  in orderDict.keys():
            orderDict[monthYear] += order['total']
            orderNoDict[monthYear] += 1
        else:
            orderDict[monthYear] = order['total']
            orderNoDict[monthYear] = 1

    print(orderDict)

    return orderDict,orderNoDict




@app.route('/user_dashboard', methods=["GET", "POST"])
def userDashboard():
    # Initialize an error message variable
    session.setdefault('error_message', [])
    
    if session.get('user_id') is None:
        session['error_message'] = "You must be logged in to view your cart"
        return redirect(url_for('login'))
    
    orderList = getOrders()

    recentOrderList = getSortedOrdersByDate('date',True)[:5]

    shippedOrderList = getShippedOrders()[:5]

    sortedProductQuantityList = getProductQuantity(orderList)[:5]

    totalExpenditure = getTotalExpenditure(orderList)

    totalQuantity = getTotalQuantity(getProductQuantity(orderList))

    maxTotal = mostExpensiveOrder(orderList)

    ordersNeedingPayment = getOrdersNeedingPayment()

    graphData = listOfExpenditureByMonth( getSortedOrdersByDate('date',True))

    arrivingOrderList = getSortedOrdersByDate('arrival_date',False)[:5]

    #chart for monthly expenditure
    colors = {
        'background': '#ffffff',
        'text': '#17252A'
    }
    expenditureData = graphData[0]
    expenditureData = pd.DataFrame({'Date':expenditureData.keys(),'Expenditure': expenditureData.values()})
    expenditureChart = px.bar(expenditureData, x="Date", y="Expenditure", color="Date", barmode="group")
    expenditureChart.update_traces(marker_color='#1d9abc',
    width=0.6)
    expenditureChart.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        bargap=0.50,
        margin_pad=20
    )

    expenditureChartHTML = expenditureChart.to_html(full_html=False)

    #chart for number of monthly ordersexpenditure
    orderNumberData = graphData[1]
    orderNumberData = pd.DataFrame({'Date':orderNumberData.keys(),'No. of Orders': orderNumberData.values()})
    orderNumberChart = px.bar(orderNumberData, x="Date", y="No. of Orders", color="Date", barmode="group")
    orderNumberChart.update_traces(marker_color='#1d9abc',
    width=0.6)
    orderNumberChart.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        bargap=0.50,
        margin_pad=20
    )





    orderNumberChartHTML = orderNumberChart.to_html(full_html=False)


    return render_template('user_dashboard.html', recentOrderList = recentOrderList , shippedOrderList = shippedOrderList, 
                           sortedProductQuantityList = sortedProductQuantityList, totalExpenditure = totalExpenditure , 
                           totalQuantity = totalQuantity,ordersNeedingPayment = ordersNeedingPayment,maxTotal=maxTotal,
                           expenditureChartHTML = expenditureChartHTML, orderNumberChartHTML = orderNumberChartHTML,arrivingOrderList=arrivingOrderList)