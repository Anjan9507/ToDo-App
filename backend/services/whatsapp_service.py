from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

FROM_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")


def send_whatsapp_message(to_number: str, message: str):
    try:
        msg = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=f"whatsapp:{to_number}"
        )
        return msg.sid
    except Exception as e:
        print("Error: ", e)
        return None