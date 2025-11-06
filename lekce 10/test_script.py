from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]
collection = db["test_collection"]

result = collection.insert_many([{"name": "Changelog", "value": True}])
print(f"Result id: {result.inserted_ids}")