from PostGresController.PostGresController import initialise_crud

create, read, update, delete = initialise_crud()

# Test query 1: Print all the suppliers.
query = read.select(table='supplier')
for record in query:
    print(record)

print('\n')

# Test query 2: Print all the suppliers where contact info ends with a 9.
query = read.select(table='supplier', where=["contactinfo LIKE '%9'", "supplierid=153"])
for record in query:
    print(record)

print('\n')

# Test query 3: Print all the suppliers where contact info ends with a 9 AND with a supplierid of 153.
query = read.select(table='supplier', where=["contactinfo LIKE '%9'", "supplierid=153"])
for record in query:
    print(record)

print('\n')

# Test query 4: Print all the users
query = read.select(table='public.user')
for record in query:
    print(query)

# Test query 5: Insert user

'''query = create.insert(table='user', 
                      columns=[
                          'username', 
                          'userpassword', 
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
                      ])'''
print('\n')

# Test query 6: Query users after insertion.
query = read.select(table='public.user')
for record in query:
    print(record)

# Test query 7: Delete records from database (with condition)
# query = delete.delete('public.user', ["username='controllerTest'"])

# Test query 8: Print all the users
query = read.select(table='public.user')
for record in query:
    print(record)

# Test query 9: Modify the username of 'controllerTest2' to 'controllerTest'.
query = update.update(
    table='user', 
    colvalues={
        'username':'controllerTest'
    },
    where=["username='controllerTest2'"]
)

# Test query 10: Modify the username of 'controllerTest' to 'Test User 1', and change address to '172 Ang Mo Kio Ave 8, Singapore 567739'
query = update.update(
    table='user',
    colvalues={
        'username':'Test User 1',
        'useraddress': '172 Ang Mo Kio Ave 8, Singapore 567739'
    },
    where=["username='controllerTest'"]
)

query = read.select(table='public.user')
for record in query:
    print(record)

query = read.select(
            'product',
            limit=20,
            orderBy={'productid': 'ASC'}
        )
for row in query:
    print(row)

query = read.select(
                'product',
                where=["productid='1'"],
            )
for row in query:
    print(row)