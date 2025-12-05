from fastapi import APIRouter
from pydantic import BaseModel
from logic import generate_personalised_tip
from typing import Optional

router = APIRouter()

class TipRequest(BaseModel):
    user_id: str
    target_savings: Optional[float] = None

@router.post("/ai/personalised-tip")
async def personalised_tip(req: TipRequest):
    tip = await generate_personalised_tip(req.user_id, req.target_savings)
    return {"status": "success", "tip": tip}
