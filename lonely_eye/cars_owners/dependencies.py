from fastapi import UploadFile, HTTPException, status


def is_valid_excel(excel_file: UploadFile):
    if excel_file.filename.endswith(".xlsx"):
        return excel_file
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=f"Expected: '.xlsx'. Received: '.{excel_file.filename.split('.')[-1]}'",
    )
