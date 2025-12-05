# AI/Assistant/backend/ai_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from data_fetcher import fetch_user_expenses
from ai_engine import run_ai_engine

router = APIRouter()

class QueryRequest(BaseModel):
    user_id: str
    query: str


@router.post("/ai/assistant")
async def ai_assistant(req: QueryRequest):
    try:
        # 1. Fetch user data from DB
        expense_data = fetch_user_expenses(req.user_id)

        # 2. Generate AI answer
        answer = run_ai_engine(req.query, expense_data)

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
