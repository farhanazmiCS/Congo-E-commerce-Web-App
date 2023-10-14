from psycopg2 import connect
import configparser

def establish_conn() -> object:
    """ Establishes a connection with the relational database """
    config = configparser.ConfigParser()
    config.read('config.ini')
    conn = connect(
        host=config['CREDENTIALS']['host'],
        database=config['CREDENTIALS']['database'],
        user=config['CREDENTIALS']['user'],
        password=config['CREDENTIALS']['password']
    )
    return conn

class Create:
    def __init__(self, connection):
        self.connection = connection
        self.cur = self.connection.cursor()

    def insert(self, table: str, columns: list, values: list) -> str:
        """ Inserts a value into a column in a table and returns the sql statement """
        columns = ','.join(columns)
        placeholders = ','.join(['%s'] * len(values))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        return self.execute(sql, values)

    def execute(self, sql, values: list):
        """ Executes the prepared statement """
        try:
            self.cur.execute(sql, values)
        except:
            print("Query cannot be executed")
        else:
            print("Success!")


class Read:
    def __init__(self, connection):
        self.connection = connection
        self.cur = self.connection.cursor()
        
    def fetch(self, table: str, columns=None, joins=None, where=None, params=None):
        """ Fetches data from a specified table and automatically executes the SQL """
        
        # Selecting all columns
        if columns is None:
            sql = f'SELECT * FROM {table}'
        else:
            columns = ','.join(columns)
            sql = f'SELECT {columns} FROM {table}'

        # Handling joins
        if joins:
            sql += self.construct_joins(joins)
            
        # Handling where conditions
        if where:
            sql += f' WHERE {where}'
            
        # Execute and fetch results
        return self.execute(sql, params)
    
    def construct_joins(self, joins):
        """ For constructing the joins """
        join_str = ''
        for join in joins:
            # Example use "JOIN products ON sid=pid"
            join_str += f" {join['type']} JOIN {join['table']} ON {join['condition']} "
        return join_str.strip()

    def execute(self, sql, params=None):
        """ Executes the SQL query """
        try:
            if params:
                self.cur.execute(sql, params)  # using parameters to avoid SQL injection
            else:
                self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            # Log or print the exception
            print(f"An error occurred: {str(e)}")
            # You might want to re-raise the exception after logging it for further upstream handling
            raise e

class Update:
    def __init__(self, connection):
        self.connection = connection
        self.cur = self.connection.cursor()
        
    def update(self, table, values, conditions):
        """ Updates a tuple in a table based on specified conditions """
        
    
    def execute(self, table, values, conditions):
        sql = self.update(table, values, conditions)
        try:
            self.cur.execute(sql, values)
        except:
            print("Query cannot be executed")
        

class Delete:
    def __init__(self, connection):
        self.connection = connection
        self.curr = self.connection.cursor()
        
    def delete(self, table, conditions=None):
        """ Deletes tuple(s) from a table """
        if conditions == None:
            return f'DELETE FROM {table}'
        else:
            return f'DELETE FROM {table} WHERE'

    def execute(self, table, conditions=None):
        sql = self.delete(table, conditions)


def initialise_crud():
    global conn, create, read, update, delete
    conn = establish_conn()
    if conn is not None:
        print("Connection established.")
        create = Create(conn)
        read = Read(conn)
        update = Update(conn)
        delete = Delete(conn)
        return create, read, update, delete
    else:
        print("Connection with database failed")
    