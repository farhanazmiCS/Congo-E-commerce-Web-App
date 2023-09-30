from sqlalchemy import create_engine
from models import Base, Product
from sqlalchemy.orm import sessionmaker


class PostgreSQLController:
    def __init__(self, url="postgresql://citus:inf2003-project@c-inf2003-project.k5sswns2zd3kt5.postgres.cosmos.azure.com:5432/citus?sslmode=require"):
        self.engine = create_engine(url)
        Base.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine)

    def add_product(self, product):
        session = self.session()
        session.add(product)
        session.commit()
        session.close()

    def get_product(self, product_id):
        session = self.session()
        try:
            return session.get(Product, product_id)
        finally:
            session.close()

    def delete_product(self, product_id):
        session = self.session()
        try:
            session.delete(session.get(Product, product_id))
            session.commit()
        finally:
            session.close()


if __name__ == "__main__":
    controller = PostgreSQLController()
    print("Get product with id 7070396835163472091")
    print(controller.get_product(7070396835163472091))
    product = Product(id=1, name="test", main_category="test", sub_category="test", image="test",
                      link="test", ratings="test", no_of_ratings="test", discount_price="test", actual_price="test")
    print("Add product with id 1")
    controller.add_product(product)

    print("Get product with id 1")
    print(controller.get_product(1))

    print("Delete product with id 1")
    controller.delete_product(1)

    print("Get product with id 1")
    print(controller.get_product(1))
