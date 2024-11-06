from fastapi import APIRouter

from src.api.v1.views import (api_user_auth_view, api_user_view, api_department_view, api_pusher_view, api_sendgrid_view, api_twilio_view)

router = APIRouter(prefix="/api/v1")

router.include_router(api_user_auth_view.router, tags=["Authentication Endpoints"])
router.include_router(api_user_view.router, tags=["User Endpoints"])
router.include_router(api_department_view.router, tags=["Department Endpoints"])
router.include_router(api_pusher_view.router, tags=["Pusher Endpoints"])
router.include_router(api_twilio_view.router, tags=["Twilio Endpoints"])