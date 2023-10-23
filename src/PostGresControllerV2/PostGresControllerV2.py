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
        
    def select(
            self, 
            table: str, 
            columns: list=[], 
            joins: list=[], 
            where: list=[], 
            distinct: bool=False, 
            orderBy: dict={}, 
            limit: int=None, 
            offset: int=None) -> object:
        """ Fetches data from a specified table and automatically executes the SQL 

            Usage examples:

                fetch(table='supplier') -> SELECT * FROM supplier
                fetch(table='supplier', columns=['suppliername'], where={'supplierid':1}) -> SELECT suppliername FROM supplier WHERE supplierid = 1 
                fetch(table='supplier', columns=['suppliername'], orderBy={'supplierName': 'DESC'}) -> SELECT suppliername FROM supplier ORDER BY suppliername DESC
                fetch(table='supplier', columns['suppliername'], limit=20, offset=20) -> SELECT suppliername FROM supplier LIMIT 20 OFFSET 20

        """
        
        # If columns parameter is empty, *
        if columns == []:
            sql = f'SELECT * FROM {table}'
        # Projection
        else:
            columns = ','.join(columns)
            if not distinct:
                sql = f'SELECT {columns} FROM {table}'
            else:
                sql = f'SELECT DISTINCT {columns} FROM {table}'

        # Handling joins
        if joins != []:
            sql += self.construct_joins(joins)
            
        # Handling where conditions
        if where != []:
            sql += self.construct_where(where)

        # Handling order by operations
        if orderBy != {}:
            for order in orderBy:
                sql += self.construct_order(order, orderBy[order])

        # Handling limit
        if limit != None:
            sql += self.construct_limit(limit)

        # Handling offset
        if offset != None:
            sql += self.construct_offset(offset)
            
        # Execute and fetch results
        return self.execute(sql)
    
    def construct_joins(self, joins) -> str:
        """ For constructing the joins """
        join_str = ''
        for join in joins:
            # Example use "JOIN products ON sid=pid"
            join_str += f" {join['type']} JOIN {join['table']} ON {join['condition']} "
        return join_str
    
    def construct_where(self, conditions) -> str:
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
    
    def construct_order(self, column: str, type: str='ASC') -> str:
        """ For constructing the order by """
        order_str = f' ORDER BY {column} {type}'
        return order_str
    
    def construct_limit(self, limit: int) -> str:
        """ For constructing limit query """
        limit_str = f' LIMIT {limit}'
        return limit_str
    
    def construct_offset(self, offset: int) -> str:
        """ For constructing offset query """
        offset_str = f' OFFSET {offset}'
        return offset_str
            
    def execute(self, sql) -> None:
        """ Executes the SQL query """
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except (Exception, DatabaseError) as e:
            # Log or print the exception
            print(f"An error occurred: {str(e)}")
            # You might want to re-raise the exception after logging it for further upstream handling
            raise e

class Update:
    def __init__(self, connection):
        self.connection = connection
        self.cur = self.connection.cursor()
        
    def update(self, table: str, colvalues: dict={}, where: list=[]) -> object:
        """ 
            Updates a tuple in a table based on specified conditions 

            Usage 1:

            Record to modify => Change 'controllerTest2' username to 'controllerTest' in the 'user' table.

            update(
                table='user', 
                colvalues={
                    'username':'controllerTest'
                },
                where=["username='controllerTest2'"]
            )

            Usage 2:

            Record to modify => Change 'controllerTest' username to 'Test User 1' and change useraddress to '172 Ang Mo Kio Ave 8, Singapore 567739'.

            query = update(
                table='user',
                colvalues={
                    'username':'Test User 1',
                    'useraddress': '172 Ang Mo Kio Ave 8, Singapore 567739'
                },
                where=["username='controllerTest'"]
            )

        """
        sql = f'UPDATE "{table}" SET'
        if colvalues != {}:
            for index, key in enumerate(colvalues):
                if index == 0:
                    sql += f" {key}='{colvalues[key]}'"
                else:
                    sql += f", {key}='{colvalues[key]}'"
        if where != []:
            sql += self.construct_where(where)
        return self.execute(sql)
    
    def construct_where(self, conditions) -> str:
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
    
    def execute(self, sql) -> None:
        try:
            self.cur.execute(sql)
            self.connection.commit()
        except (Exception, DatabaseError) as e:
            # Rollback if execution fails
            self.connection.rollback()
            print(f"Error: {e}")
        
class Delete:
    def __init__(self, connection):
        self.connection = connection
        self.cur = self.connection.cursor()
        
    def delete(self, table, conditions=[]) -> object:
        """ Deletes tuple(s) from a table 

            Usage examples:

            delete('public.user') -> DELETE FROM public.user
            delete('public.user', ["username='controllerTest']) -> DELETE FROM public.user WHERE username='controllerTest'
        
        """
        sql = f'DELETE FROM {table}'
        if conditions != []:
            sql += f'{self.construct_where(conditions)}'
        return self.execute(sql)
        
    def construct_where(self, conditions) -> str:
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

    def execute(self, sql) -> None:
        """ Executes the SQL query """
        try:
            self.cur.execute(sql)
            self.connection.commit()
        except (Exception, DatabaseError) as e:
            # Rollback if execution fails
            self.connection.rollback()
            # Log or print the exception
            print(f"An error occurred: {e}")


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
    