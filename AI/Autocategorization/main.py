from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_extractor import LLMExtractor
from db_writer import DBWriter

app = FastAPI()

# Initialize once
extractor = LLMExtractor()
writer = DBWriter()

# Pydantic model for request
class ExpenseRequest(BaseModel):
    user_id: str
    paragraph: str

@app.post("/api/auto-categorize")
def auto_categorize(data: ExpenseRequest):
    """
    Client sends:
    {
        "user_id": "user123",
        "paragraph": "I bought pizza 250, Uber ride 180, coffee 90 today."
    }
    """
    try:
        # 1️⃣ LLM extraction
        expenses = extractor.extract(data.paragraph)

        # 2️⃣ Directly store in DB
        result = writer.insert_expenses(user_id=data.user_id, expenses=expenses)

        # 3️⃣ Return inserted expenses to client
        return {"status": "success", "inserted_count": result["inserted_count"], "expenses": expenses}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
