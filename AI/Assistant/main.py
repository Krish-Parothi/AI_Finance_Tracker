# AI/Assistant/backend/main.py

from fastapi import FastAPI
from ai_route import router as ai_router

app = FastAPI()

# Register routes
app.include_router(ai_router, prefix="/api", tags=["AI-Assistant"])
