from fastapi import FastAPI
from bill_expense_route import router as bill_router

app = FastAPI()

app.include_router(bill_router, prefix="/api/whatsapp")
# main.py