import PostGresController as PostGresController
from sqlalchemy import URL, create_engine
import configparser
import os
from sqlalchemy import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import time
from sqlalchemy.sql import func


# The application's PostGresController.
create, read, update, delete = PostGresController.initialise_crud()


def time_postgrescontroller():
    start_time = time.time()
    read.select(
            columns=['productimg'],
            table='product',
            joins=[{'type': 'INNER', 'table': 'subcategory', 'condition': 'product.subcategoryid = subcategory.subcategoryid'},
                {'type': 'INNER', 'table': 'category', 'condition': 'subcategory.categoryid = category.categoryid'}],
            where=[f'category.categoryid = 1'],
            orderBy={'RANDOM()': 'LIMIT 1'}
        )
    end_time = time.time()
    return round((end_time - start_time) * 1000, 0)

# Connect to the same database using SQLAlchemy
script_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)

url_object = URL.create(
    drivername="postgresql+psycopg2",
    username=config['CREDENTIALS']['user'],
    password=config['CREDENTIALS']['password'],
    host=config['CREDENTIALS']['host'],
    database=config['CREDENTIALS']['database'],
)

engine = create_engine(url_object)

Base = automap_base()
Base.prepare(engine, reflect=True)

session = Session(engine)

Product = Base.classes.product
Subcategory = Base.classes.subcategory
Category = Base.classes.category

def time_sqlalchemy():
    start_time = time.time()
    query = session.query(Product.productimg).join(Subcategory, Product.subcategoryid == Subcategory.subcategoryid).join(Category, Subcategory.categoryid == Category.categoryid).filter(Category.categoryid == 1).order_by(func.random()).limit(1)
    query.one_or_none()
    end_time = time.time()
    return round((end_time - start_time) * 1000, 0)

print('PG\tAL\tWIN\tDELTA')

sum_pg = 0
average_pg = 0
sum_al = 0
average_al = 0
run = 50

for _ in range(run):
    postgres_controller_time = time_postgrescontroller()
    sqlalchemy_time = time_sqlalchemy()

    # Determine which is faster
    if postgres_controller_time < sqlalchemy_time:
        faster = "PG"
    elif sqlalchemy_time < postgres_controller_time:
        faster = "AL"
    elif sqlalchemy_time == postgres_controller_time:
        faster = "="
    
    sum_pg += postgres_controller_time
    sum_al += sqlalchemy_time

    print(f"{postgres_controller_time:.0f}ms\t{sqlalchemy_time:.0f}ms\t{faster}\t{abs(postgres_controller_time - sqlalchemy_time)} ms")

print(f"\nAverage execution time for PG: {sum_pg / run} ms")
print(f"\nAverage execution time for AL: {sum_al / run} ms")
print(f"\nAverage difference in execution time between PG and AL: {round(abs(sum_pg / run - sum_al / run), 2)} ms")

if sum_pg / run < sum_al / run:
    print(f"\nPG is faster than AL")
elif sum_al / run < sum_pg / run:
    print(f"\nAL is faster than PG")
else:
    print(f"\nTied")