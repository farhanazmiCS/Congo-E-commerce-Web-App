import os
from psycopg2 import connect, DatabaseError
import configparser

def establish_conn() -> object:
    """ Establishes a connection with the relational database """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(script_dir, 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_file)

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

    def insert(self, table: str, columns: list, values: list) -> object:
        """ Inserts a value into a column in a table and returns the sql statement 
        
            Usage example:

            insert(table='user', 
                      columns=[
                          'username', 
                          'userpasword', 
                          'usertype', 
                          'useremail', 
                          'useraddress'
                        ], 
                      values=[
                          'controllerTest2',
                          'HASHED_PASSWORD',
                          'customer',
                          'controllertest2@test.com',
                          '510 Dover Rd, Singapore 139660'
                      ])    
        """
        columns = ','.join(columns)
        placeholders = ','.join(['%s'] * len(values))
        sql = f'INSERT INTO "{table}" ({columns}) VALUES ({placeholders})'
        return self.execute(sql, values)

    def execute(self, sql: str, values: list) -> None:
        """ Executes the prepared statement """
        try:
            self.cur.execute(sql, values)
            self.connection.commit()
        except (Exception, DatabaseError) as e:
            self.connection.rollback()
            print(f'Error {e}')
        else:
            print("Record successfully added into table")


class Read:
    def __init__(self, connection):
        self.connection = connection
        self.cur = self.connection.cursor()
        
    def fetch(self, table: str, columns: list=[], joins: list=[], where: list=[]) -> object:
        """ Fetches data from a specified table and automatically executes the SQL 

            Usage examples:

                fetch(table='supplier') -> SELECT * FROM supplier
                fetch(table='supplier', columns=['suppliername'], where={'supplierid':1}) -> SELECT suppliername FROM supplier WHERE supplierid = 1 

        """
        
        # If columns parameter is empty, *
        if columns == []:
            sql = f'SELECT * FROM {table}'
        # Projection
        else:
            columns = ','.join(columns)
            sql = f'SELECT {columns} FROM {table}'

        # Handling joins
        if joins != []:
            sql += self.construct_joins(joins)
            
        # Handling where conditions
        if where != []:
            sql += self.construct_where(where)
            
        # Execute and fetch results
        return self.execute(sql)
    
    def construct_joins(self, joins):
        """ For constructing the joins """
        join_str = ''
        for join in joins:
            # Example use "JOIN products ON sid=pid"
            join_str += f" {join['type']} JOIN {join['table']} ON {join['condition']} "
        return join_str.strip()
    
    def construct_where(self, conditions):
        """ For constructing the where """
        where_str = ''
        for index, where in enumerate(conditions):
            if index == 0:
                where_str += f' WHERE {where}'
            elif index != conditions[-1]:
                where_str += f'AND {where}'
            else:
                where_str += f'{where}'
        return where_str
            

    def execute(self, sql):
        """ Executes the SQL query """
        try:
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
        self.cur = self.connection.cursor()
        
    def delete(self, table, conditions=[]):
        """ Deletes tuple(s) from a table 

            Usage examples:

            delete('public.user') -> DELETE FROM public.user
            delete('public.user', ["username='controllerTest']) -> DELETE FROM public.user WHERE username='controllerTest'
        
        """
        sql = f'DELETE FROM {table}'
        if conditions != []:
            sql += f'{self.construct_where(conditions)}'
        return self.execute(sql)
        
    def construct_where(self, conditions):
        """ For constructing the where """
        where_str = ''
        for index, where in enumerate(conditions):
            if index == 0:
                where_str += f' WHERE {where}'
            elif index != conditions[-1]:
                where_str += f'AND {where}'
            else:
                where_str += f'{where}'
        return where_str

    def execute(self, sql):
        """ Executes the SQL query """
        try:
            self.cur.execute(sql)
            self.connection.commit()
        except Exception as e:
            # Rollback if execution fails
            self.connection.rollback()
            # Log or print the exception
            print(f"An error occurred: {str(e)}")
            # You might want to re-raise the exception after logging it for further upstream handling
            raise e


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
    