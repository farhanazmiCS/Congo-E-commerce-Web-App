from PostGresControllerV2 import initialise_crud

create, read, update, delete = initialise_crud()

# Test
print(read.fetch('product'))