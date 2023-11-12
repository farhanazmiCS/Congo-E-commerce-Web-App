import PostGresControllerV2
from sqlalchemy import create_engine

# The application's PostGresController.
create, read, update, delete = PostGresControllerV2.initialise_crud()
