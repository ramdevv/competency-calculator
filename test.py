from pymongo import MongoClient
from bson import ObjectId
-
mongo_server = MongoClient("mongodb://localhost:27017")
ccc_db = mongo_server.ccc_database

user_collection = ccc_db.user
score_collection = ccc_db.score

INSERT_ID = "67ec0d30979b5e07c05284a3"

results = score_collection.find_one({"_id": ObjectId(INSERT_ID)})
print(results)
