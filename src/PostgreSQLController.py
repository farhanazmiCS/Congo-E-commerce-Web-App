from sqlalchemy import create_engine
from models import Base, Product
from sqlalchemy.orm import sessionmaker


class PostgreSQLController:
    """
    A class used to interact with a PostgreSQL database using SQLAlchemy.

    Attributes
    ----------
    engine : sqlalchemy.engine.Engine
        The engine used to connect to the database.
    session : sqlalchemy.orm.Session
        The session used to interact with the database.

    Methods
    -------
    add_product(product: Product) -> None:
        Adds a product to the database.
    get_product(product_id: int) -> Product:
        Retrieves a product from the database by its ID.
    delete_product(product_id: int) -> None:
        Deletes a product from the database by its ID.
    """

    def __init__(self, url="postgresql://citus:inf2003-project@c-inf2003-project.k5sswns2zd3kt5.postgres.cosmos.azure.com:5432/citus?sslmode=require"):
        """
        Constructs a new PostgreSQLController object.

        Parameters
        ----------
        url : str, optional
            The URL used to connect to the database, by default "postgresql://citus:inf2003-project@c-inf2003-project.k5sswns2zd3kt5.postgres.cosmos.azure.com:5432/citus?sslmode=require"
        """
        self.engine = create_engine(url)
        Base.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine)

    def add_product(self, product: Product) -> None:
        """
        Adds a product to the database.

        Parameters
        ----------
        product : Product
            The product to add to the database.
        """
        session = self.session()
        session.add(product)
        session.commit()
        session.close()

    def get_product(self, product_id: int) -> Product:
        """
        Retrieves a product from the database by its ID.

        Parameters
        ----------
        product_id : int
            The ID of the product to retrieve.

        Returns
        -------
        Product
            The product with the specified ID.
        """
        session = self.session()
        try:
            return session.get(Product, product_id)
        finally:
            session.close()

    def delete_product(self, product_id: int) -> None:
        """
        Deletes a product from the database by its ID.

        Parameters
        ----------
        product_id : int
            The ID of the product to delete.
        """
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
