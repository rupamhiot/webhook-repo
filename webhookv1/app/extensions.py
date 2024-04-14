from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongo:27017")
db = client['webhook_data']
collection = db['events']