from fastapi import HTTPException, status


no_case = HTTPException(
    status_code=status.HTTP_418_IM_A_TEAPOT,
    detail="No cases",
)

permission_denied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied",
)
