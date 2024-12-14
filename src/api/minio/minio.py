from fastapi import HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse
from src.storage.minio_client import download_file


from src.logger import logger
from .router import router
from starlette import status
from io import BytesIO


@router.get("/get-file", summary="Скачать файл")
async def get_file(
    user_id: int = Query(..., description="ID пользователя"),
    file_name: str = Query(..., description="Имя файла")
) -> StreamingResponse:
    """
    Скачивает файл из MinIO и возвращает его в виде потока байтов.

    Args:
        user_id (int): ID пользователя.
        file_name (str): Имя файла.

    Returns:
        StreamingResponse: Файл в виде потока байтов.
    """
    # Поиск записи файла в базе данных
    # async with async_session() as db:
    #     result = await db.execute(
    #         select(FileRecord).where(FileRecord.user_id == user_id, FileRecord.file_name == file_name)
    #     )
    #     file_record = result.scalar_one_or_none()

    # if file_record is None:
    #     logger.error("Файл не найден в базе данных.")
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл не найден.")



    # logger.info("""Файл {} найден в базе данных""".format(file_name)+ """ID пользователя: {}""".format(user_id) + """Путь к файлу: {}""".format(file_record.file_path))

    # Получаем путь к файлу в MinIO
    minio_path = f"{user_id}_{file_name}"
    
    # local_path = f"/tmp/{file_name}"

    # Скачиваем файл из MinIO
    try:
        # Загружаем файл в байтах
        file_bytes = await download_file(minio_path)
        logger.info(f"Файл {file_name} скачан из MinIO.")
    except Exception as e:
        logger.error(f"Ошибка при скачивании файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при скачивании файла.")

    # Возвращаем файл пользователю
    return StreamingResponse(
            file_bytes,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file_name}"}
        )
    # не работает передача туда file_bytes
    # return FileResponse(file_bytes, filename=file_name) # bytesio = io .BytesIO(bytes)