# AI/Assistant/engine/db.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["finance_db"]
expenses_collection = db["expenses"]
