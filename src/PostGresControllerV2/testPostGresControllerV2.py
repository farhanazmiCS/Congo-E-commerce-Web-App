from PostGresControllerV2 import initialise_crud

create, read, update, delete = initialise_crud()

# Test query 1: Print all the suppliers.
query = read.fetch(table='supplier')
for record in query:
    print(record)

print('\n')

# Test query 2: Print all the suppliers where contact info ends with a 9.
query = read.fetch(table='supplier', where=["contactinfo LIKE '%9'"])
for record in query:
    print(record)

print('\n')

# Test query 3: Print all the users
query = read.fetch(table='user')
for record in query:
    print(query)

# Test query 4: Insert user

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

query = read.fetch(table='public.user')
for record in query:
    print(record)

