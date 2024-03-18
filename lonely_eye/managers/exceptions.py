from fastapi import HTTPException, status


activate_worker_username_wrong = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Username invalid"
)
