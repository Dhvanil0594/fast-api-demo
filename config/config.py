import os

SECRET_KEY = os.getenv("SECRET_KEY", "this-is-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 500

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:root@localhost:3306/test_alembic")
