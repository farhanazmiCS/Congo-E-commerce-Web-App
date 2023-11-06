import os
import pandas as pd
import random
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey, func
from sqlalchemy.orm import declarative_base, Session

# Define the database connection string
db_connection_string = "postgresql://citus:inf2003-project@c-inf2003-project.k5sswns2zd3kt5.postgres.cosmos.azure.com:5432/citus?sslmode=require"

# Create a SQLAlchemy engine
engine = create_engine(db_connection_string)

# Create a base class for declarative models
Base = declarative_base()

# Define the User table
class User(Base):
    __tablename__ = "user"

    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    userpassword = Column(String, nullable=False)
    usertype = Column(String, nullable=False)
    useremail = Column(String, nullable=False)
    useraddress = Column(String, nullable=False)

# Define the Order table
class Order(Base):
    __tablename__ = "order"

    orderid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.userid"), nullable=False)
    orderdate = Column(Date, nullable=False)
    ordertotal = Column(Numeric(10, 2), nullable=False)

# Define the OrderStatus table
class OrderStatus(Base):
    __tablename__ = "orderstatus"

    orderstatusid = Column(Integer, primary_key=True, autoincrement=True)
    orderid = Column(Integer, ForeignKey("order.orderid"), nullable=False)
    orderstatusname = Column(String, nullable=False)
    orderstatusdescription = Column(String, nullable=False)
    shippeddate = Column(Date)

# Define the Supplier table
class Supplier(Base):
    __tablename__ = "supplier"

    supplierid = Column(Integer, primary_key=True, autoincrement=True)
    suppliername = Column(String, nullable=False)
    contactinfo = Column(String, nullable=False)

# Define the SubCategory table
class SubCategory(Base):
    __tablename__ = "subcategory"

    subcategoryid = Column(Integer, primary_key=True, autoincrement=True)
    categoryid = Column(Integer, ForeignKey("category.categoryid"), nullable=False)
    subcategoryname = Column(String, nullable=False)
    subcategorydescription = Column(String, nullable=False)

# Define the Category table
class Category(Base):
    __tablename__ = "category"

    categoryid = Column(Integer, primary_key=True, autoincrement=True)
    categoryname = Column(String, nullable=False)
    categorydescription = Column(String, nullable=False)

# Define the Product_JX table
class Product(Base):
    __tablename__ = "product"

    productid = Column(Integer, primary_key=True, autoincrement=True)
    productname = Column(String, nullable=False)
    productdesc = Column(String)
    productimg = Column(String)
    productprice = Column(Numeric(10, 2), nullable=False)
    productstock = Column(Integer, nullable=False)
    supplierid = Column(Integer, ForeignKey("supplier.supplierid"), nullable=False)
    subcategoryid = Column(Integer, ForeignKey("subcategory.subcategoryid"), nullable=False)
    productrating = Column(Numeric(3, 2), nullable=False, default=0.00)

# Create the tables in the database
Base.metadata.create_all(engine)

''' IMPORT: Category / Subcategory '''
# Start a new session
session = Session(bind=engine)

# Create empty lists for main categories and sub-categories
main_categories = []
sub_categories = []

# Specify the Amazon Products CSV file
file = 'Amazon-Products.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(os.path.join('data', file))

# Get the unique sub_categories and main_categories from the DataFrame
unique_main_categories = df['main_category'].unique()
unique_sub_categories = df[['main_category', 'sub_category']].drop_duplicates().values.tolist()

# Create empty lists for main categories and sub-categories
main_categories = []
sub_categories = []

# Iterate over each main_category
for main_category_name in unique_main_categories:
    main_categories.append(main_category_name )

# Iterate over each unique main-sub_category pair
for main_category_name, sub_category_name in unique_sub_categories:
    sub_categories.append((main_category_name, sub_category_name))

# Import Main Category to Postgres
for main_category_name in main_categories:
    main_category = Category(
        categoryname=main_category_name,
        categorydescription=main_category_name
    )
    session.add(main_category)
    session.commit()

# Import Sub Category to Postgres
for (main_category_name, sub_category_name) in sub_categories:
    # Get the MainCategoryID of the current sub_category
    main_category_id = session.query(Category.categoryid).filter_by(categoryname=main_category_name).first()[0]
    
    sub_category = SubCategory(
        subcategoryname=sub_category_name,
        subcategorydescription=sub_category_name,
        categoryid=main_category_id
    )
    session.add(sub_category)
    session.commit()

''' IMPORT: Supplier '''
# Get CSV
file = 'Fake_Company.csv'

# Read the CSV file into a DataFrame
supplier_df = pd.read_csv(os.path.join('data', file))

# Iterate over each row in the DataFrame and insert data into the Supplier table
for index, row in supplier_df.iterrows():
    supplier = Supplier(
        suppliername=row['ComapanyName'],
        contactinfo=row['Contact']
    )
    session.add(supplier)
    session.commit()

''' IMPORT: Products '''
# Import Product Info to Postgres
file = 'Amazon-Products.csv'

# Read the CSV file into a DataFrame
amazon_csv = pd.read_csv(os.path.join('data', file))
amazon_csv.drop_duplicates(inplace=True) # Remove the duplicates
amazon_csv.dropna(inplace=True) # Remove the rows with missing values

# Get the range for supplierid by querying the Supplier table
min_supplier_id = session.query(func.min(Supplier.supplierid)).scalar()
max_supplier_id = session.query(func.max(Supplier.supplierid)).scalar()
print(min_supplier_id, max_supplier_id)

# Get a list of subcategories with their IDs and names to cache them
subcategories = session.query(SubCategory.subcategoryid, SubCategory.subcategoryname).all()
subcategory_cache = {row.subcategoryname: row.subcategoryid for row in subcategories}
print(subcategory_cache)

# Create a list to store Product objects
products = []

# Iterate over each row in the DataFrame and prepare data
for index, row in amazon_csv.iterrows():
    product = Product(
        productname=row['name'],
        productdesc="Description for " + row['name'],
        productimg=row['image'].replace('W/IMAGERENDERING_521856-T1/images/', '').replace('W/IMAGERENDERING_521856-T2/images/', ''), # Fix for invalid image URL
        productprice = min(round(float(row['actual_price'].replace('₹', '').replace(',', '')) * 0.016, 2), 10**8 - 0.01), # Convert and round price, cap at maximum price
        productstock=random.randint(0, 500),  # Random stock value
        supplierid=random.randint(min_supplier_id, max_supplier_id),  # Random supplier ID
        subcategoryid=subcategory_cache.get(row['sub_category'])  # Use cached subcategory ID
    )
    products.append(product)

# Add all products to the session
session.add_all(products)

# Commit the transaction
session.commit()

# Close the session
session.close()