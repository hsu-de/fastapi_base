from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

client = MongoClient("mongodb://root:rootpassword@localhost:27017/")
async_client = AsyncIOMotorClient("mongodb://root:rootpassword@localhost:27017/")

db = client.todo_db
async_db = async_client.todo_db

# collection_name = db['todo_collection']
# async_collection = async_db['todo_collection']