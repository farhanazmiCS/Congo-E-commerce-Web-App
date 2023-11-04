import pymongo
import pandas as pd

class MongoDBController:
    # def __init__(self, connection_uri, database_name=None):
    #     self.client = pymongo.MongoClient(connection_uri)
    #     if database_name:
    #         self.db = self.client[database_name]
    #     else:
    #         raise ValueError("A database name must be provided")
        
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://inf2003-project:9XygVh5kKnrscIiKfsPXCos1KtjQtFSmMcZfwod9O22zosZE3ZUHrVVbtSQs262Jvv5IwpiFeOUWACDbJsgL2A==@inf2003-project.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000&appName=@inf2002003-project@")
        self.db = self.client["test"]


    def create(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_one(data)

    def read(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find(query)
    
    def aggregate(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.aggregate(query)

    def update(self, collection_name, query, new_data):
        collection = self.db[collection_name]
        return collection.update_one(query, {"$set": new_data})

    def delete(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.delete_one(query)

    def list_collections(self):
        return self.db.list_collection_names()

    def close_connection(self):
        self.client.close()

    def insert_csv_data(self, collection_name, csv_file):
        collection = self.db[collection_name]
        data = pd.read_csv(csv_file)
        data_dict = data.to_dict(orient='records')
        return collection.insert_many(data_dict)




if __name__ == "__main__":
    # Replace the connection URI and database name with your own
    connection_uri = "mongodb://inf2003-project:9XygVh5kKnrscIiKfsPXCos1KtjQtFSmMcZfwod9O22zosZE3ZUHrVVbtSQs262Jvv5IwpiFeOUWACDbJsgL2A==@inf2003-project.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000&appName=@inf2002003-project@"
    database_name = "test"

    controller = MongoDBController(connection_uri, database_name)

    # controller.create("Cart", {"userid": 1, "products": []})

    # # Insert data from Air Conditioners CSV
    # controller.insert_csv_data("air_conditioners", "Air Conditioners.csv")

    # # Insert data from All Books CSV
    # controller.insert_csv_data("all_books", "All Appliances.csv")

    controller.close_connection()