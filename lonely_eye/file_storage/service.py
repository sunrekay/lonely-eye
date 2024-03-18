import boto3
from botocore.exceptions import ClientError

from lonely_eye.config import settings

s3 = boto3.client(
    aws_access_key_id=settings.storage.aws_access_key_id,
    aws_secret_access_key=settings.storage.aws_secret_access_key,
    service_name=settings.storage.service_name,
    endpoint_url=settings.storage.endpoint_url,
)


def get_photo_url(
    bucket_name: str,
    file_name: str,
    expiration: int = settings.storage.expiration_url_seconds,
) -> str | None:
    try:
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": file_name},
            ExpiresIn=expiration,
        )
        return response
    except ClientError as e:
        return None


def upload_photo(
    file,
    file_name: str,
    bucket_name: str,
):
    try:
        s3.upload_fileobj(
            Fileobj=file,  # open("img-test.jpg", "rb"),  # File to download
            Bucket=bucket_name,  # Bucket
            Key=file_name,  # Object name
        )
        return True
    except Exception:
        return False
