from fastapi import HTTPException, status

wrong_login_password = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
)

problem_with_redis_connection = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Please, try again later...",
)

refresh_token_invalid = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Refresh-Token invalid",
)

wrong_token = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Wrong JWT-Token",
)

permission_denied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied",
)

worker_inactive = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Worker inactive",
)
