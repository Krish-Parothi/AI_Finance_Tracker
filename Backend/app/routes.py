# app/routes.py
from flask import Blueprint, request, jsonify
from app.controllers import signup, login

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/signup", methods=["POST"])
def signup():
    data = request.json
    response = signup(
        data["username"],
        data["email"],
        data["password"]
    )
    return jsonify(response)

@user_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    response = login(
        data["email"],
        data["password"]
    )
    return jsonify(response)
