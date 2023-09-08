import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
client = pymongo.MongoClient(CONNECTION_STRING)

for prop, value in vars(client.options).items():
    print("Property: {}: Value: {} ".format(prop, value))

# Create a database and collection
db = client["test-database"]
collection = db["test-collection"]
collection.insert_one({"name": "test"})

print(client.list_database_names())
print(db.list_collection_names())
documents = collection.find()
for doc in documents:
    print(doc)