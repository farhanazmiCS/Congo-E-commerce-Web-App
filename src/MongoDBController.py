from pymongo import MongoClient


class MongoDBController:
    """
    A class used to interact with a MongoDB database.

    ...

    Attributes
    ----------
    url : str
        The URL of the MongoDB database.

    Methods
    -------
    add_product(product)
        Adds a product to the database.
    get_product(product_id)
        Retrieves a product from the database.
    delete_product(product_id)
        Deletes a product from the database.
    """

    def __init__(self, url="mongodb://localhost:27017/"):
        """
        Constructs a new MongoDBController object.

        Parameters
        ----------
        url : str, optional
            The URL of the MongoDB database (default is "mongodb://localhost:27017/").
        """
        self.client = MongoClient(url)
        self.db = self.client["test"]

    def add_product(self, product):
        """
        Adds a product to the database.

        Parameters
        ----------
        product : dict
            A dictionary representing the product to be added.
        """
        collection = self.db["product"]
        collection.insert_one(product)

    def get_product(self, product_id):
        """
        Retrieves a product from the database.

        Parameters
        ----------
        product_id : int
            The ID of the product to be retrieved.

        Returns
        -------
        dict
            A dictionary representing the retrieved product.
        """
        collection = self.db["product"]
        return collection.find_one({"id": product_id})

    def delete_product(self, product_id):
        """
        Deletes a product from the database.

        Parameters
        ----------
        product_id : int
            The ID of the product to be deleted.
        """
        collection = self.db["product"]
        collection.delete_one({"id": product_id})


if __name__ == "__main__":
    controller = MongoDBController()
    print("Get product with id 7070396835163472091")
    print(controller.get_product(7070396835163472091))

    product = {"id": 1, "name": "test", "main_category": "test", "sub_category": "test", "image": "test",
               "link": "test", "ratings": "test", "no_of_ratings": "test", "discount_price": "test", "actual_price": "test"}
    print("Add product with id 1")
    controller.add_product(product)

    print("Get product with id 1")
    print(controller.get_product(1))

    print("Delete product with id 1")
    controller.delete_product(1)

    print("Get product with id 1")
    print(controller.get_product(1))
