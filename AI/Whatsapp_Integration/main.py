from fastapi import FastAPI
from Text_Expense.text_expense_route import router as text_router
from Bill_Expense.bill_expense_route import router as bill_router

app = FastAPI()

app.include_router(text_router, prefix="/api/whatsapp/text")
app.include_router(bill_router, prefix="/api/whatsapp/bill")

# main.py