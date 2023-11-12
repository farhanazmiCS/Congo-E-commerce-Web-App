import PostGresController.PostGresController as PostGresController
from sqlalchemy import create_engine

# The application's PostGresController.
create, read, update, delete = PostGresController.initialise_crud()
