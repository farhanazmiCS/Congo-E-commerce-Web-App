from pymongo import MongoClient


class MongoDBController:
    def __init__(self, url="mongodb://inf2003-project:9XygVh5kKnrscIiKfsPXCos1KtjQtFSmMcZfwod9O22zosZE3ZUHrVVbtSQs262Jvv5IwpiFeOUWACDbJsgL2A==@inf2003-project.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@inf2003-project@"):
        self.client = MongoClient(url)
        self.db = self.client["test"]

    def add_product(self, product):
        collection = self.db["product"]
        collection.insert_one(product)

    def get_product(self, product_id):
        collection = self.db["product"]
        return collection.find_one({"id": product_id})

    def delete_product(self, product_id):
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
