# bill_expense_route.py
from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from bill_parser import parse_bill
from expense_service import add_expense
import requests
import tempfile
import os

router = APIRouter()

@router.post("/webhook")
async def bill_webhook(MediaUrl0: str = Form(...), From: str = Form(...)):
    # Download image from Twilio MediaUrl
    try:
        response = requests.get(MediaUrl0)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(response.content)
            local_path = tmp.name
    except Exception as e:
        resp = MessagingResponse()
        resp.message(f"Failed to download image: {str(e)}")
        return PlainTextResponse(str(resp), media_type="application/xml")

    # Upload to a public URL or file server that your Groq model can access
    # Here we assume you have a function that returns a public URL from local path
    # For demo, using local_path directly, but in production you must host it publicly
    public_url = f"file://{local_path}"

    entries = parse_bill(public_url)
    for entry in entries:
        add_expense(From, entry)

    resp = MessagingResponse()
    resp.message("Expense added successfully")
    # clean up temporary file
    os.unlink(local_path)
    return PlainTextResponse(str(resp), media_type="application/xml")
#bill_expense.py