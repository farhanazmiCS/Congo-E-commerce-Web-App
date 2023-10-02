import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

# Define the database connection string
db_connection_string = "postgresql://citus:inf2003-project@c-inf2003-project.k5sswns2zd3kt5.postgres.cosmos.azure.com:5432/citus?sslmode=require"

# Create a SQLAlchemy engine
engine = create_engine(db_connection_string)

# Create a base class for declarative models
Base = declarative_base()

# Define the User table
class User(Base):
    __tablename__ = "User"

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    UserName = Column(String, nullable=False)
    UserPassword = Column(String, nullable=False)
    UserType = Column(String, nullable=False)
    UserEmail = Column(String, nullable=False)
    UserAddress = Column(String, nullable=False)

# Define the Order table
class Order(Base):
    __tablename__ = "Order"

    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    OrderDate = Column(Date, nullable=False)
    OrderTotal = Column(Numeric(10, 2), nullable=False)

# Define the OrderStatus table
class OrderStatus(Base):
    __tablename__ = "OrderStatus"

    OrderStatusID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey("Order.OrderID"), nullable=False)
    OrderStatusName = Column(String, nullable=False)
    OrderStatusDescription = Column(String, nullable=False)
    ShippedDate = Column(Date)

# Define the Supplier table
class Supplier(Base):
    __tablename__ = "Supplier"

    SupplierID = Column(Integer, primary_key=True, autoincrement=True)
    SupplierName = Column(String, nullable=False)
    ContactInfo = Column(String, nullable=False)

# Define the SubCategory table
class SubCategory(Base):
    __tablename__ = "SubCategory"

    SubCategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryID = Column(Integer, ForeignKey("Category.CategoryID"), nullable=False)
    SubCategoryName = Column(String, nullable=False)
    SubCategoryDescription = Column(String, nullable=False)

# Define the Category table
class Category(Base):
    __tablename__ = "Category"

    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String, nullable=False)
    CategoryDescription = Column(String, nullable=False)

# Define the Product_JX table
class Product_JX(Base):
    __tablename__ = "Product_JX"

    ProductID = Column(Integer, primary_key=True, autoincrement=True)
    ProductName = Column(String, nullable=False)
    ProductDesc = Column(String)
    ProductPrice = Column(Numeric(10, 2), nullable=False)
    ProductStock = Column(Integer, nullable=False)
    SupplierID = Column(Integer, ForeignKey("Supplier.SupplierID"), nullable=False)
    SubCategoryID = Column(Integer, ForeignKey("SubCategory.SubCategoryID"), nullable=False)

# Create the tables in the database
Base.metadata.create_all(engine)

# Import Categories
# Start a new session
session = Session(bind=engine)

# Create empty lists for main categories and sub-categories
main_categories = []
sub_categories = []

# Specify the CSV file
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

# Import to Postgres
for main_category_name in main_categories:
    main_category = Category(
        CategoryName=main_category_name,
        CategoryDescription=main_category_name
    )
    session.add(main_category)
    session.commit()

for (main_category_name, sub_category_name) in sub_categories:
    # Get the MainCategoryID of the current sub_category
    main_category_id = session.query(Category.CategoryID).filter_by(CategoryName=main_category_name).first()[0]
    
    sub_category = SubCategory(
        SubCategoryName=sub_category_name,
        SubCategoryDescription=sub_category_name,
        CategoryID=main_category_id
    )
    session.add(sub_category)
    session.commit()

# Close the session
session.close()

''' for debug:
DROP TABLE IF EXISTS "Category" CASCADE;
DROP TABLE IF EXISTS "Order" CASCADE;
DROP TABLE IF EXISTS "OrderStatus" CASCADE;
DROP TABLE IF EXISTS "User" CASCADE;
DROP TABLE IF EXISTS "SubCategory" CASCADE;
DROP TABLE IF EXISTS "Supplier" CASCADE;
DROP TABLE IF EXISTS "Product_JX" CASCADE;
'''