from fastapi import APIRouter, FastAPI, HTTPException, status
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config.config import settings
import os

router = APIRouter(prefix="/send-email")

@router.post("/", status_code=status.HTTP_200_OK)
async def send_email(to_email: str, subject: str, message: str):
    try:
        # Create the email content
        email = Mail(
            from_email='dhvanil.prajapati@mindinventory.com',  # Use a verified sender email
            to_emails=to_email,
            subject=subject,
            html_content=f"<p>{message}</p>"
        )
        
        # Initialize SendGrid client and send the email
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(email)

        # Return success message
        return {"message": "Email sent successfully", "status_code": response.status_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
