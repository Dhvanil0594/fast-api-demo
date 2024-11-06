from fastapi import APIRouter, FastAPI, HTTPException, status
from config.config import settings
from twilio.rest import Client

router = APIRouter(prefix="/send-sms")

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@router.post("/")
async def send_sms(to: str, message: str):
    """Endpoint to send an SMS"""
    from_phone_number = settings.TWILIO_PHONE_NUMBER  # Replace with your Twilio number

    try:
        message = client.messages.create(
            body=message,
            from_=from_phone_number,
            to=to
        )
        return {"status": "success", "message_sid": message.sid}
    except Exception as e:
        return {"status": "error", "message": str(e)}