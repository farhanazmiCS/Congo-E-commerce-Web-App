from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
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

    def to_dict(self):
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

    def __repr__(self):
        return "<Product(id='%s', name='%s', main_category='%s', sub_category='%s', image='%s', link='%s', ratings='%s', no_of_ratings='%s', discount_price='%s', actual_price='%s')>" % (
            self.id, self.name, self.main_category, self.sub_category, self.image, self.link, self.ratings, self.no_of_ratings, self.discount_price, self.actual_price)
