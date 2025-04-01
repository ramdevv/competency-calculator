from pymongo import MongoClient


mongo_server = MongoClient("mongodb://mongodb:27017")
ccc_db = mongo_server.ccc_database

user_collection = ccc_db.user
score_collection = ccc_db.score
