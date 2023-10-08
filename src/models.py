from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    """
    A class representing a product.

    Attributes:
    -----------
    id : int
        The unique identifier of the product.
    name : str
        The name of the product.
    main_category : str
        The main category of the product.
    sub_category : str
        The sub category of the product.
    image : str
        The URL of the product's image.
    link : str
        The URL of the product's page.
    ratings : str
        The rating of the product.
    no_of_ratings : str
        The number of ratings the product has received.
    discount_price : str
        The discounted price of the product.
    actual_price : str
        The actual price of the product.
    """
    __tablename__ = 'product'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    main_category = Column(String)
    sub_category = Column(String)
    image = Column(String)
    link = Column(String)
    ratings = Column(String)
    no_of_ratings = Column(String)
    discount_price = Column(String)
    actual_price = Column(String)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the product.
        """
        return {
            "id": self.id,
            "name": self.name,
            "main_category": self.main_category,
            "sub_category": self.sub_category,
            "image": self.image,
            "link": self.link,
            "ratings": self.ratings,
            "no_of_ratings": self.no_of_ratings,
            "discount_price": self.discount_price,
            "actual_price": self.actual_price
        }

    def __repr__(self) -> str:
        """
        Returns a string representation of the product.
        """
        return "<Product(id='%s', name='%s', main_category='%s', sub_category='%s', image='%s', link='%s', ratings='%s', no_of_ratings='%s', discount_price='%s', actual_price='%s')>" % (
            self.id, self.name, self.main_category, self.sub_category, self.image, self.link, self.ratings, self.no_of_ratings, self.discount_price, self.actual_price)
