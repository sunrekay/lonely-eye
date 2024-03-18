from typing import Any

import bcrypt
import jwt
from jwt import ExpiredSignatureError
from fastapi import HTTPException, status

from lonely_eye.auth.schemas import TokensInfo, RefreshToken, AccessToken
from lonely_eye.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    try:
        return jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )


def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password=password.encode(),
        salt=bcrypt.gensalt(),
    )


def verify_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def tokens_info(model: Any, refresh_token_id: str) -> TokensInfo:
    return TokensInfo(
        access_token=encode_jwt(
            payload=AccessToken(
                sub=str(model.id),
                username=model.username,
            ).model_dump()
        ),
        refresh_token=encode_jwt(
            payload=RefreshToken(
                sub=str(model.id),
                username=model.username,
                token_id=refresh_token_id,
            ).model_dump()
        ),
    )
