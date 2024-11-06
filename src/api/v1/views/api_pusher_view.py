from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database.database import get_db
from src.api.v1.schemas import user_schemas as _US
from src.api.v1.models.user_models import user_info as _UI
from logger import logger
from fastapi.security import OAuth2PasswordBearer
from src.api.v1.repositories import api_department_repository as _DR
from src.api.v1.repositories import api_user_repository as _UR
from src.api.v1.services.pusher_service import pusher_client

router = APIRouter(prefix="/send-notification")

@router.post("/")
async def send_notification(channel: str, event: str, title: str, message: str):
    try:
        # Send a notification event with a title and message
        pusher_client.trigger(channel, event, {
            'title': title,
            'message': message
        })
        return {"status": "Notification sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
