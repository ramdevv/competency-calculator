from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client.test_database

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
}
table = db.table
post_id = table.insert_one(post).inserted_id
print(post_id)
