# AI/Assistant/engine/data_fetcher.py

from db import expenses_collection

def fetch_user_expenses(user_id: str):
    """
    Fetch all expenses of the user.
    """
    data = list(expenses_collection.find({"user_id": user_id}, {"_id": 0}))
    return data
