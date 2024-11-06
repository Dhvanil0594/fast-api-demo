# import os

# SECRET_KEY = os.getenv("SECRET_KEY", "this-is-secret")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 500

# DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:root@localhost:3306/test_alembic")
from pydantic_settings import BaseSettings, SettingsConfigDict
from logger import logger
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DEBUG: bool = False
    PROFILING_ENABLED: bool = False
    OPENAPI_DOCS_URL: str | None = None
    OPENAPI_REDOC_URL: str | None = None
    MASTER_DB_USER: str
    MASTER_DB_PASSWORD: str
    MASTER_DB_HOSTNAME: str
    MASTER_DB_PORT: str
    MASTER_DB_NAME: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 500
    ALGORITHM: str
    PUSHER_APP_ID: str
    PUSHER_KEY: str
    PUSHER_SECRET: str
    PUSHER_CLUSTER: str
    SENDGRID_API_KEY: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str


settings = Settings()