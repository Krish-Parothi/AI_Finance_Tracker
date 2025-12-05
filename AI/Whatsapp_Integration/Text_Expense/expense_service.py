from datetime import datetime
from db import expense_collection   # adjust import to your structure

def add_expense(user_phone: str, expense_data: dict):
    expense_record = {
        "user_phone": user_phone,
        "amount": expense_data.get("amount"),
        "category": expense_data.get("category"),
        "description": expense_data.get("description"),
        "timestamp": expense_data.get("timestamp"),
        "source": expense_data.get("source", "whatsapp"),
        "metadata": expense_data.get("metadata", {}),
        "created_at": datetime.utcnow().isoformat()
    }
 
    result = expense_collection.insert_one(expense_record)

    return str(result.inserted_id)
#expense_service.py