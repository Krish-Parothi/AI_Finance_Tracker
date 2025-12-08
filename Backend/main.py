# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_handler import register_exception_handlers
from app.routers import auth, expenses, analytics, llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(llm.router, prefix="/llm", tags=["llm"])
