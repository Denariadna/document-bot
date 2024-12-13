from fastapi import HTTPException, Query
from fastapi.responses import FileResponse
from src.storage.minio_client import download_file, get_file_path
from src.storage.db import async_session
from src.model.meta import FileRecord
from sqlalchemy.future import select
from src.logger import logger
from .router import router

@router.get("/get-file", summary="Скачать файл")
async def get_file(
    user_id: int = Query(..., description="ID пользователя"),
    file_name: str = Query(..., description="Имя файла")
) -> FileResponse:
    """
    Скачивает файл из MinIO и возвращает его.

    Args:
        user_id (int): ID пользователя.
        file_name (str): Имя файла.

    Returns:
        FileResponse: Файл для скачивания.
    """
    # Поиск записи файла в базе данных
    async with async_session() as db:
        result = await db.execute(
            select(FileRecord).where(FileRecord.user_id == user_id, FileRecord.file_name == file_name)
        )
        file_record = result.scalar_one_or_none()

    if file_record is None:
        logger.error("Файл не найден в базе данных.")
        raise HTTPException(status_code=404, detail="Файл не найден.")

    # Получаем путь к файлу в MinIO
    minio_path = file_record.file_path
    local_path = f"/tmp/{file_name}"

    # Скачиваем файл из MinIO
    try:
        await download_file(minio_path, local_path)
        logger.info(f"Файл {file_name} скачан из MinIO.")
    except Exception as e:
        logger.error(f"Ошибка при скачивании файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при скачивании файла.")

    # Возвращаем файл пользователю
    return FileResponse(local_path, filename=file_name)
