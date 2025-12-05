from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os 

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["finance_app"]

expenses_collection = db["expenses"]