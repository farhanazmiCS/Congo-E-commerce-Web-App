import pandas as pd
import os
import psycopg2
from psycopg2 import pool
import psycopg2.extras as extras
import pandas as pd

def execute_values(conn, cursor, df, table):
    # Create table (id,name,main_category,sub_category,image,link,ratings,no_of_ratings,discount_price,actual_price)
    cursor.execute("CREATE TABLE IF NOT EXISTS %s (id BIGINT PRIMARY KEY, name varchar, main_category varchar, sub_category varchar, image varchar, link varchar, ratings varchar, no_of_ratings varchar, discount_price varchar, actual_price varchar);" % (table))
    tuples = [tuple(x) for x in df.to_numpy()]
    
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()

# Build a connection string from the variables
CONNECTION_STRING = "host=c-inf2003-project.k5sswns2zd3kt5.postgres.cosmos.azure.com port=5432 dbname=citus user=citus password=inf2003-project sslmode=require"

data_path = "/workspaces/INF2003-Project/data"

# Import all the csv files into the dataframe
df = pd.concat(map(pd.read_csv, [os.path.join(data_path, f) for f in os.listdir(
    data_path) if f.endswith('.csv')]), ignore_index=True)
print("Shape of the dataframe: ", df.shape)

# Remove the duplicates
df.drop_duplicates(inplace=True)
print("Shape of the dataframe after removing duplicates: ", df.shape)

# Remove the rows with missing values
df.dropna(inplace=True)
print("Shape of the dataframe after removing rows with missing values: ", df.shape)

# Generate a unique positve id for each row using hash function
df['id'] = df.apply(lambda x: abs(hash(tuple(x))), axis=1)
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
print("Shape of the dataframe after adding id: ", df.shape)
print("The first 5 rows of the dataframe: ")
print(df.head())

# Create a connection pool
postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,CONNECTION_STRING)
if (postgreSQL_pool):
    print("Connection pool created successfully")

# Use getconn() to get a connection from the connection pool
conn = postgreSQL_pool.getconn()

# Allow to execute PostgreSQL command
cursor = conn.cursor()

# Create a table
# execute_values(conn, cursor, df, 'product')

# Show size of the table
cursor.execute("SELECT COUNT(*) FROM product;")
records = cursor.fetchall()
print("Size of the table: ", records[0][0])

conn.commit()
conn.close()
