import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db_name = os.getenv("DB_NAME", "HealthLabs")
        
        try:
            self.client = MongoClient(mongodb_uri)
            self.db = self.client[db_name]
            print("Connected to MongoDB successfully")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
    
    def get_collection(self, collection_name):
        return self.db[collection_name]