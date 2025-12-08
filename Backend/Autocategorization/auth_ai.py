from fastapi import APIRouter, Response, Depends, HTTPException
from pydantic import BaseModel
import jwt, os
from datetime import datetime, timedelta
from llm import LLMExtractor
from db import DBWriter

router = APIRouter()
SECRET = os.getenv("JWT_SECRET")
extractor = LLMExtractor()
writer = DBWriter()

class LoginReq(BaseModel):
    username: str
    password: str

class ParagraphReq(BaseModel):
    paragraph: str

def create_token(data, minutes=60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=minutes)
    return jwt.encode(payload, SECRET, algorithm="HS256")

def get_current_user(token: str = Depends(lambda req: req.cookies.get("access_token"))):
    if not token:
        raise HTTPException(401, "Not authenticated")
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(401, "Invalid token")

@router.post("/login")
def login(req: LoginReq, response: Response):
    if req.username != "user" or req.password != "pass":
        raise HTTPException(401, "Invalid credentials")
    user = {"user_id": "user123", "username": req.username}
    token = create_token(user)
    response.set_cookie("access_token", token, httponly=True, secure=False, samesite="lax")
    return {"status": "logged in", "user_id": user["user_id"]}

@router.post("/auto-categorize")
def auto_categorize(data: ParagraphReq, user=Depends(get_current_user)):
    expenses = extractor.extract(data.paragraph)
    count = writer.insert_expenses(user_id=user["user_id"], expenses=expenses)
    return {"inserted": count, "parsed": expenses}
