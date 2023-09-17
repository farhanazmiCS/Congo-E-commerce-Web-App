import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
client = pymongo.MongoClient(CONNECTION_STRING)

for prop, value in vars(client.options).items():
    print("Property: {}: Value: {} ".format(prop, value))

# Create a database and collection
db = client["taylor_swift"]
collection = db["taylor_swift"]
collection.insert_one({"name": "test"})
# Add another collection to the database
db.create_collection("taylor_swift_2")

print(client.list_database_names())
print(db.list_collection_names())
documents = collection.find()
for doc in documents:
    print(doc)