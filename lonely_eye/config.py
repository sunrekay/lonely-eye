import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Boto3 Storage
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SERVICE_NAME = os.getenv("SERVICE_NAME")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")


class DBSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = True


class StorageSettings(BaseModel):
    aws_access_key_id: str = AWS_ACCESS_KEY_ID
    aws_secret_access_key: str = AWS_SECRET_ACCESS_KEY
    service_name: str = SERVICE_NAME
    endpoint_url: str = ENDPOINT_URL


class Settings(BaseSettings):

    api_title: str = "RTU_IT_Lab"

    api_prefix: str = "/api/v1"

    db: DBSettings = DBSettings()

    storage: StorageSettings = StorageSettings()


settings = Settings()
