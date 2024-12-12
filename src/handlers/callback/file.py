# from aiogram.types import CallbackQuery, Message
# from aiohttp import ClientSession
# from src.logger import logger
# from .router import router

# @router.callback_query(lambda call: call.data.startswith("file:"))
# async def handle_file_selection(callback: CallbackQuery) -> None:
#     if callback.data is None or callback.message is None:
#         logger.error("Ошибка: callback не содержит данных.")
#         return
#     file_name = callback.data.split(":", 1)[1]
#     user_id = callback.from_user.id

#     try:
#         async with ClientSession() as session:
#             async with session.get(
#                 f"http://document-bot.duckdns.org/api/minio/get-file-url",
#                 params={"user_id": user_id, "file_name": file_name}
#             ) as response:
#                 if response.status == 200:
#                     file_url = str(response.url)
#                     await callback.message.answer_document(file_url, caption=f"Ваш файл: {file_name}")
#                 else:
#                     logger.error(f"Ошибка API: {response.status}")
#                     await callback.message.answer("Ошибка при получении ссылки.")
#     except Exception as e:
#         logger.error(f"Ошибка при отправке файла: {e}")
#         await callback.message.answer("Произошла ошибка.")


from aiogram.types import CallbackQuery, Message
from src.storage.minio_client import get_file_path  # Функция для получения подписанного URL
from src.storage.db import async_session
from src.model.meta import FileRecord
from src.logger import logger

from .router import router

from sqlalchemy.future import select

@router.callback_query(lambda call: call.data.startswith("file:"))
async def handle_file_selection(callback: CallbackQuery) -> None:
    """
    Обрабатывает выбор файла из списка.
    Загружает файл из MinIO и отправляет его пользователю.
    """
    if callback.data is None or callback.message is None:
        logger.error("Ошибка: callback не содержит данных.")
        return
    file_name = callback.data.split(":", 1)[1] 

    if callback.from_user is None:
        logger.error("Ошибка: callback не содержит информации об отправителе (from_user = None).")
        return

    user_id = callback.from_user.id
    async with async_session() as db:
        result = await db.execute(
            select(FileRecord).where(FileRecord.user_id == user_id, FileRecord.file_name == file_name)
        )
        file_record = result.scalar_one_or_none()

    if file_record is None:
        await callback.message.edit_text("Файл не найден.") if isinstance(callback.message, Message) else None
        return

    # Получаем подписанный URL для скачивания файла из MinIO
    file_url = get_file_path(file_record.file_path)

    logger.info("Пользователь выбрал файл: %s", file_record.file_name)
    logger.info("Подписанный URL: %s", file_url)

    try:
        # Отправляем файл пользователю через URL
        await callback.message.answer_document(file_url, caption=f"Вы выбрали файл: {file_record.file_name}")
        await callback.answer("Файл успешно отправлен!")  # Подтверждение пользователю
    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        await callback.message.answer("Произошла ошибка при отправке файла.")
