# db_writer.py
# Purpose: Insert LLM-extracted expenses into MongoDB users database

from pymongo import MongoClient
from datetime import datetime
import os

# ---------- CONFIG ----------
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "finance_tracker"
COLLECTION_NAME = "user_expenses"


class DBWriter:
    def __init__(self, mongo_uri=MONGO_URI):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def insert_expenses(self, user_id: str, expenses: list):
        """
        Insert multiple expense records for a specific user.
        Each expense should be a dict with:
        amount, category, description, merchant, date, created_at
        """
        if not expenses:
            return {"inserted_count": 0, "status": "No expenses to insert"}

        # Add user_id and timestamp
        for item in expenses:
            item["user_id"] = user_id
            if "created_at" not in item:
                item["created_at"] = str(datetime.now())

        result = self.collection.insert_many(expenses)
        return {"inserted_count": len(result.inserted_ids), "status": "success"}

    def fetch_expenses(self, user_id: str, limit=50):
        """
        Fetch latest expenses for a user (optional helper)
        """
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return list(cursor)


# # ----------------- Example Usage -----------------
# if __name__ == "__main__":
#     writer = DBWriter()
#     sample_user_id = "user123"
#     sample_expenses = [
#         {"amount": 250, "category": "Food", "description": "pizza", "merchant": None, "date": "today"},
#         {"amount": 180, "category": "Travel", "description": "Uber ride", "merchant": "Uber", "date": "today"},
#         {"amount": 90, "category": "Food", "description": "coffee", "merchant": None, "date": "today"}
#     ]

#     result = writer.insert_expenses(sample_user_id, sample_expenses)
#     print(result)
#     print("Latest expenses:", writer.fetch_expenses(sample_user_id))
