from fastapi import HTTPException, status


wrong_bytes_line = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Wrong bytes",
)

wrong_camera_key = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Camera-Key invalid",
)

too_many_requests = HTTPException(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Please try again later...",
)

wrong_violation_key = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Violation id invalid",
)

wrong_transport_number = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Transport number invalid",
)
