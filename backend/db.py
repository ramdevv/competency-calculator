from pymongo import MongoClient
import os


MONGO_URI = os.environ["MONGO_URI"]

mongo_server = MongoClient(MONGO_URI)
ccc_db = mongo_server.ccc_database

user_collection = ccc_db.user
score_collection = ccc_db.score
