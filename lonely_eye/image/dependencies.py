from fastapi import HTTPException, UploadFile, status

from lonely_eye.image.schemas import Photo


def is_valid_photo_format(photo: UploadFile):
    photo_formats: list = Photo.formats()
    for pf in photo_formats:
        if pf in photo.content_type:
            return photo

    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=f"Expected: {', '.join(photo_formats)}. Received: {photo.filename.split('.')[-1]}",
    )
