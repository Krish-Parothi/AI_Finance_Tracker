# bill_parser.py
import json
from datetime import datetime
from groq import Groq
import os
import requests
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

def download_twilio_image(media_url: str) -> str:
    resp = requests.get(media_url, auth=(TWILIO_SID, TWILIO_TOKEN))
    resp.raise_for_status()
    return b64encode(resp.content).decode("utf-8")  # returns base64 string

def parse_bill(media_url: str):
    # download Twilio image and convert to base64
    img_base64 = download_twilio_image(media_url)

    user_prompt = f"""
You are a strict JSON extractor. You will receive a base64 encoded image of a bill, receipt, or product.
Extract the following fields with exact types:

- "amount": numeric value of the total expense.
- "category": one of ["food", "travel", "shopping", "hotel", "medical", "utilities", "other"].
- "description": concise summary of what the expense is for.
- "timestamp": ISO 8601 UTC string of the expense; if not available, use current UTC time.
- "source": string, always "whatsapp_image".
- "metadata": object, can be empty if no extra info.

Return exactly one valid JSON object with only these keys. Do not add extra text, explanations, or formatting.

Image (base64): {img_base64}
"""

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )

    try:
        raw = completion.choices[0].message["content"].strip()
        data = json.loads(raw)
        if not isinstance(data, list):
            data = [data]
    except:
        data = [{
            "amount": None,
            "category": "other",
            "description": "unparsed image",
            "timestamp": datetime.utcnow().isoformat(),
            "source": "whatsapp_image",
            "metadata": {}
        }]

    for entry in data:
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.utcnow().isoformat()
        entry["source"] = "whatsapp_image"

    return data
#bill_parser.py
