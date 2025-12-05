# app/controllers.py
from app.database import user_collection
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def signup(data):
    # Check if email exists
    if user_collection.find_one({"email": data["email"]}):
        return {"success": False, "message": "Email already exists"}

    hashed_pw = generate_password_hash(data["password"])

    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_pw
    )

    user_collection.insert_one(user.to_dict())
    return {"success": True, "message": "User registered successfully"}

def login(data):
    user = user_collection.find_one({"email": data["email"]})

    if not user:
        return {"success": False, "message": "User not found"}

    if not check_password_hash(user["password"], data["password"]):
        return {"success": False, "message": "Wrong password"}

    return {"success": True, "message": "Login successful"}
