from fastapi import FastAPI
from text_expense_route import router as text_expense_router

app = FastAPI()

app.include_router(text_expense_router, prefix="/api/whatsapp")
#main.py
