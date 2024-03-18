from fastapi import HTTPException, status
from jwt import DecodeError

from lonely_eye.auth import utils


def get_data_from_token(token: str) -> dict:
    try:
        data = utils.decode_jwt(token=token)
        return data
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token invalid",
        )
