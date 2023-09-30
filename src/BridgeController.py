from PostgreSQLController import PostgreSQLController
from MongoDBController import MongoDBController
from models import Product

class BridgeController:
    def __init__(self):
        self.pg_controller = PostgreSQLController()
        self.mongo_controller = MongoDBController()

    def add_product_to_both(self, product):
        # Convert product object to dictionary
        product_dict = product.to_dict()
        self.pg_controller.add_product(product)
        self.mongo_controller.add_product(product_dict)

    def get_product_from_both(self, product_id):
        return self.pg_controller.get_product(product_id), self.mongo_controller.get_product(product_id)
    
    def delete_product_from_both(self, product_id):
        self.pg_controller.delete_product(product_id)
        self.mongo_controller.delete_product(product_id)

    def get_product_from_pg(self, product_id):
        return self.pg_controller.get_product(product_id)
    
    def get_product_from_mongo(self, product_id):
        return self.mongo_controller.get_product(product_id)
    
    def delete_product_from_pg(self, product_id):
        self.pg_controller.delete_product(product_id)

    def delete_product_from_mongo(self, product_id):
        self.mongo_controller.delete_product(product_id)

if __name__ == "__main__":
    controller = BridgeController()
    print("Get product with id 7070396835163472091")
    print(controller.get_product_from_both(7070396835163472091))
    print(controller.get_product_from_pg(7070396835163472091))
    print(controller.get_product_from_mongo(7070396835163472091))

    product = Product(id=1, name="test", main_category="test", sub_category="test", image="test",
                      link="test", ratings="test", no_of_ratings="test", discount_price="test", actual_price="test")
    print("Add product with id 1")
    controller.add_product_to_both(product)

    print("Get product with id 1")
    print(controller.get_product_from_both(1))
    print(controller.get_product_from_pg(1))
    print(controller.get_product_from_mongo(1))

    print("Delete product with id 1")
    controller.delete_product_from_both(1)

    print("Get product with id 1")
    print(controller.get_product_from_both(1))
    print(controller.get_product_from_pg(1))
    print(controller.get_product_from_mongo(1))