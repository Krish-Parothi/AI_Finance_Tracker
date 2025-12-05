# from twilio.rest import Client
# from config import TWILIO_NUMBER
# import os
# from dotenv import load_dotenv

# load_dotenv()

# ACCOUNT_SID = os.getenv("ACCOUNT_SID")
# AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# client = Client(ACCOUNT_SID, AUTH_TOKEN)

# def send_whatsapp_reply(to, message):
#     client.messages.create(
#         from_=TWILIO_NUMBER,
#         to=to,
#         body=message
#     )


## twilio_utils.py