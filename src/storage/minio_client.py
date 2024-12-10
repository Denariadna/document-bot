from minio import Minio
from minio.error import S3Error
from config.settings import settings

minio_client = Minio(
    settings.MINIO_URL.replace("http://", "").replace("https://", ""),
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)

def create_bucket() -> None:
    if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
        minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

def upload_file(user_id: int, file_name: str, file_data: bytes) -> str:
    unique_name = f"{user_id}_{file_name}"
    minio_client.put_object(
        settings.MINIO_BUCKET_NAME, unique_name, file_data, length=len(file_data),
    )
    return unique_name

def get_file_path(file_name: str) -> str:
    return minio_client.presigned_get_object(settings.MINIO_BUCKET_NAME, file_name)
