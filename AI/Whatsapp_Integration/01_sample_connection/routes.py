# from fastapi import APIRouter, Request
# from twilio_utils import send_whatsapp_reply

# router = APIRouter()

# @router.post("/whatsapp/webhook")
# async def whatsapp_webhook(request: Request):
#     data = await request.form()
#     print("Incoming WhatsApp Message:", data)
    
#     sender = data.get("From")
#     message = data.get("Body", "")
#     if sender and message:
#         send_whatsapp_reply(sender, f"Received: {message}")
#     return "OK"


## rotes.py