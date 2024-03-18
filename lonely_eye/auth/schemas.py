from datetime import datetime, timedelta

from pydantic import BaseModel

from lonely_eye.config import settings


class AccessToken(BaseModel):
    sub: str
    username: str
    exp: datetime = datetime.utcnow() + timedelta(
        minutes=settings.auth_jwt.access_token_expire_minutes
    )
    iat: datetime = datetime.utcnow()


class RefreshToken(BaseModel):
    sub: str
    username: str
    token_id: str
    exp: datetime = datetime.utcnow() + timedelta(
        minutes=settings.auth_jwt.refresh_token_expire_minutes
    )
    iat: datetime = datetime.utcnow()


class TokensInfo(BaseModel):
    access_token: str
    refresh_token: str
    tokens_type: str = "Bearer"
