from PostGresControllerV2 import initialise_crud

create, read, update, delete = initialise_crud()

# Test query 1: Print all the suppliers.
query = read.fetch(table='supplier')
for record in query:
    print(record)

print('\n')

# Test query 2: Print all the suppliers where contact info ends with a 9.
query = read.fetch(table='supplier', where=["contactinfo LIKE '%9'", "supplierid=153"])
for record in query:
    print(record)

print('\n')

# Test query 3: Print all the suppliers where contact info ends with a 9 AND with a supplierid of 153.
query = read.fetch(table='supplier', where=["contactinfo LIKE '%9'", "supplierid=153"])
for record in query:
    print(record)

print('\n')

# Test query 4: Print all the users
query = read.fetch(table='public.user')
for record in query:
    print(query)

# Test query 5: Insert user

'''query = create.insert(table='user', 
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
                      ])'''
print('\n')

# Test query 6: Query users after insertion.
query = read.fetch(table='public.user')
for record in query:
    print(record)

# Test query 7: Delete records from database (with condition)
# query = delete.delete('public.user', ["username='controllerTest'"])

# Test query 8: Print all the users
query = read.fetch(table='public.user')
for record in query:
    print(record)