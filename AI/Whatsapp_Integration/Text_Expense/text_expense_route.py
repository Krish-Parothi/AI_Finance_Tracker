from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import logging
from llm_parser import parse_text
from expense_service import add_expense

logging.basicConfig(level=logging.INFO)
router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    logging.info(f"Received from {From}: {Body}")  # confirm endpoint is hit
    parsed_entries = parse_text(Body)
    for entry in parsed_entries:
        add_expense(From, entry)


    resp = MessagingResponse()
    resp.message("Expense added successfully")

    return PlainTextResponse(str(resp), media_type="application/xml")

#text_expense_rote.py