# INF2003-Project

## Project description
This project involves the creation and implementation of an E-commerce website. It's designed to showcase robust user and administrative functionality, handling large-scale data management and dynamic product categorization. Key features include:
- Cart System: A user-friendly interface for adding and managing products in a shopping cart.
- Order System: Efficient processing and tracking of customer orders.
- Product Management: Administrative capabilities to manage the vast array of products.
- Review System: Allows users to leave reviews, enhancing the shopping experience and providing valuable feedback.

## Run the project
This project is best run in Docker to ensure all dependencies are met. To run the project, simply follow these steps:
1. Install Docker and VSCode Dev Containers extension.
2. Clone the repository.
3. Open the project in VSCode.
4. Open the command palette (Ctrl+Shift+P) and select "Remote-Containers: Reopen in Container".
5. Open a terminal in VSCode and run the following commands:
```
python congoDB.py
```
6. Open a browser and navigate to http://127.0.0.1:5000

## Importing of Data to Database
If running from scratch, ensure the dependencies are installed and configured (Python with libraries in requirements.txt installed, PostgreSQL and MongoDB backends configured).

To create the base tables in the relational database and import the data from the Kaggle Amazon Dataset into the database, run the `createTables.py` file in the `src/init` folder. The consolidated Amazon product dataset is available in `Amazon-Products.csv`, and the fake company details are in `Fake_Company.csv`, which are located in the `src/init/data` folder.

For the non-relational database (MongoDB), ensure that `Cart`, `Orders` and `Reviews` collections are created.

## Performance Test Scripts
Performance test scripts used for this product are located in:
- `src/performance_test/product_test.py` (Test the performance between querying product details via SQL, and via SQL + NoSQL)
- `src/controller/PostGresControllerAnalysis.py` (Test the performance between our controller vs SQLAlchemy)
