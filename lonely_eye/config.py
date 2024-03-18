import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SERVICE_NAME = os.getenv("SERVICE_NAME")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")


class DBSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False  # TODO: Before production, change from True to False


class StorageSettings(BaseModel):
    aws_access_key_id: str = AWS_ACCESS_KEY_ID
    aws_secret_access_key: str = AWS_SECRET_ACCESS_KEY
    service_name: str = SERVICE_NAME
    endpoint_url: str = ENDPOINT_URL

    expiration_url_seconds: int = 3600

    worker_photo_storage_name: str = "lonely-eye-workers"
    cases_photo_storage_name: str = "lonely-eye-cases"

    photo_format: str = "png"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"

    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379

    worker_photo_url_expire_seconds: int = int(
        StorageSettings().expiration_url_seconds * 0.8
    )
    case_photo_url_expire_seconds: int = int(
        StorageSettings().expiration_url_seconds * 0.8
    )

    refresh_token_expire_seconds: int = AuthJWT().refresh_token_expire_minutes * 60


class Settings(BaseSettings):

    api_title: str = "RTU_IT_Lab"
    api_prefix: str = "/api/v1"

    db: DBSettings = DBSettings()

    redis: RedisSettings = RedisSettings()

    storage: StorageSettings = StorageSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
