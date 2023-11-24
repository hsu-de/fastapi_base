from pymongo import MongoClient

client = MongoClient("mongodb://root:rootpassword@localhost:27017/")

db = client.todo_db

collection_name = db['todo_collection']