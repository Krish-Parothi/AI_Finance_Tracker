from flask import Blueprint, request, jsonify
from datetime import datetime
from bson.objectid import ObjectId
from expense_model import expenses_collection

expense_bp = Blueprint("expense_bp", __name__)

@expense_bp.route("/add", methods=["POST"])
def add_expense():
    data = request.get_json()

    # required fields check
    required = ["amount", "category", "date", "user_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    try:
        expense = {
            "amount": float(data["amount"]),
            "category": data["category"],
            "date": datetime.strptime(data["date"], "%Y-%m-%d"),
            "note": data.get("note", ""),
            "user_id": ObjectId(data["user_id"])
        }

        result = expenses_collection.insert_one(expense)

        return jsonify({
            "message": "Expense added successfully",
            "expense_id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


    # ✔ This API = /expense/add
    # ✔ It adds an expense
    # ✔ Saves it in MongoDB