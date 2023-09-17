import psycopg2
from psycopg2 import pool

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

# Create a table
cursor.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")

# Show all table
cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
tables = cursor.fetchall()
for table in tables:
    print(table[0])

# Insert data
cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (200, "abc'def"))
cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (300, "abc'def"))

# Show all data
cursor.execute("SELECT * FROM test;")
records = cursor.fetchall()
for record in records:
    print(record)

# Delete data
cursor.execute("DELETE FROM test WHERE num = %s", (100,))
cursor.execute("DELETE FROM test WHERE num = %s", (200,))
cursor.execute("DELETE FROM test WHERE num = %s", (300,))
cursor.execute("SELECT * FROM test;")
records = cursor.fetchall()
if not records:
    print("No data in table")
else:
    for record in records:
        print(record)

# Clean up
conn.commit()
cursor.close()
conn.close()