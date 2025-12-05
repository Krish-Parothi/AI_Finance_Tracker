# app/main.py
from flask import Flask
from flask_cors import CORS
from app.routes import user_routes
from expenses.expenses_routes import expense_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Auth Routes
    app.register_blueprint(user_routes, url_prefix="/api/user")

    # Expense Routes
    app.register_blueprint(expense_bp, url_prefix="/api/expense")

    return app
