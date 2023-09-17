import psycopg2
from psycopg2 import pool

PASSWORD = "inf2003-project"

# Build a connection string from the variables
CONNECTION_STRING = "host=c-inf2003-project.k5sswns2zd3kt5.postgres.cosmos.azure.com port=5432 dbname=citus user=citus password=inf2003-project sslmode=require"

# Create a connection pool
postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,CONNECTION_STRING)
if (postgreSQL_pool):
    print("Connection pool created successfully")

# Use getconn() to get a connection from the connection pool
conn = postgreSQL_pool.getconn()

# Allow to execute PostgreSQL command
cursor = conn.cursor()

# Import all the csv file in ../data into database
import os
import glob
import csv
path = "/workspaces/INF2003-Project/data"
allFiles = glob.glob(os.path.join(path,"*.csv"))

for file in allFiles:
    # Get the name of the file
    fileName = os.path.basename(file)
    print(fileName)
    # Get the name of the table and convert it to lowercase and space to underscore
    tableName = fileName.split(".")[0].lower().replace(" ", "_")
    print(tableName)
    # Create a table based on the name of the file and the first row of the file
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(header)
        # Create a table
        cursor.execute("CREATE TABLE IF NOT EXISTS " + tableName + " (" + " varchar, ".join(header) + " varchar);")
        # Insert data
        for row in reader:
            cursor.execute("INSERT INTO " + tableName + " (" + ", ".join(header) + ") VALUES (" + ", ".join(["%s"] * len(header)) + ")", row)



# Show all table
cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
tables = cursor.fetchall()
for table in tables:
    print(table[0])

# Clean up
conn.commit()
cursor.close()
conn.close()