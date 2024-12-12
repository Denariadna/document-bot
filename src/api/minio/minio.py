from fastapi import HTTPException, Query
from fastapi.responses import RedirectResponse
from src.storage.minio_client import get_file_path
from src.storage.db import async_session
from src.model.meta import FileRecord
from sqlalchemy.future import select
from src.logger import logger
from .router import router


@router.get("/get-file-url", summary="Получить URL файла")
async def get_file_url(
    user_id: int = Query(..., description="ID пользователя"),
    file_name: str = Query(..., description="Имя файла")
) -> RedirectResponse:
    """
    Возвращает публичный URL для скачивания файла из MinIO.

    Args:
        user_id (int): ID пользователя.
        file_name (str): Имя файла.

    Returns:
        RedirectResponse: Перенаправление на подписанный URL.
    """
    async with async_session() as db:
        result = await db.execute(
            select(FileRecord).where(FileRecord.user_id == user_id, FileRecord.file_name == file_name)
        )
        file_record = result.scalar_one_or_none()

    if file_record is None:
        logger.error("Файл не найден в базе данных.")
        raise HTTPException(status_code=404, detail="Файл не найден.")

    signed_url = get_file_path(file_record.file_path)
    logger.info(f"Подписанный URL для {file_name}: {signed_url}")

    return RedirectResponse(signed_url)
