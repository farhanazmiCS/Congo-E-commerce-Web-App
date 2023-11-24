from datetime import datetime
import math
import time  # Import the time module for measuring time

import sys
import os

# Calculate the path to the src directory
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)

# Add the src directory to sys.path
if src_dir not in sys.path:
    sys.path.append(src_dir)

import controller.PostGresController as pg
import controller.mongodbController as mg


create, read, update, delete = pg.initialise_crud()
mgdb = mg.MongoDBController()

def get_product_details(product_id):
    product_details = read.select(
        table='product',
        where=[f'productid = {product_id}'])
    return product_details
    
# Function to get product details and measure the time taken
def get_product_and_measure_time(product_id):
    start_time = time.time()  # Record the start time

    product_details = get_product_details(product_id)

    end_time = time.time()  # Record the end time

    # Calculate the time taken in milliseconds
    elapsed_time_ms = (end_time - start_time) * 1000

    return elapsed_time_ms

# Function to get product details from MongoDB and measure the time taken
def get_product_and_measure_time_mongo(product_id):
    start_time = time.time()  # Record the start time

    product_details = get_product_details(product_id)
    
    result = list(mgdb.read('Reviews', {'productID': product_id}))
    if len(result):
        rating = str(result[0].get('rating', 0))  # Return the average rating if found

    end_time = time.time()  # Record the end time

    # Calculate the time taken in milliseconds
    elapsed_time_ms = (end_time - start_time) * 1000

    return elapsed_time_ms

# Function to perform SQL queries and calculate the average time
def perform_sql_queries():
    elapsed_times = []
    # Discard the first result
    get_product_and_measure_time(178603) # Don't count initial lag time
    for _ in range(12):  # Run the loop 50 more times
        elapsed_time = get_product_and_measure_time(178603)
        elapsed_times.append(elapsed_time)
        print(f"Time taken to query product (SQL): {elapsed_time:.2f} ms")
    
    return elapsed_times

# Function to perform NoSQL (MongoDB) queries and calculate the average time
def perform_mongo_queries():
    elapsed_times = []
    # Discard the first result
    get_product_and_measure_time_mongo(178603) # Don't count initial lag time
    for _ in range(12):  # Run the loop 50 more times
        elapsed_time = get_product_and_measure_time_mongo(178603)
        elapsed_times.append(elapsed_time)
        print(f"Time taken to query product (SQL + NoSQL): {elapsed_time:.2f} ms")
    
    return elapsed_times

# Call the functions to perform the tests
sql_elapsed_times = perform_sql_queries()
mongo_elapsed_times = perform_mongo_queries()

# Calculate and print the average time for SQL queries
average_sql_time = sum(sql_elapsed_times) / len(sql_elapsed_times)
print(f"Average time taken for SQL queries (12 times): {average_sql_time:.2f} ms")

# Calculate and print the average time for MongoDB queries
average_mongo_time = sum(mongo_elapsed_times) / len(mongo_elapsed_times)
print(f"Average time taken for SQL + NoSQL queries (12 times): {average_mongo_time:.2f} ms")