from aiogram.types import CallbackQuery
from aiogram.types.input_file import BufferedInputFile  # Импортируем правильный класс для работы с файлами
from config.settings import settings
from src.logger import logger
from aiohttp import ClientSession
import io

from .router import router

@router.callback_query(lambda call: call.data.startswith("file:"))
async def handle_file_selection(callback: CallbackQuery) -> None:
    """
    Обрабатывает выбор файла из списка.
    Загружает файл из MinIO и отправляет его пользователю через Telegram.
    """
    if callback.data is None or callback.message is None:
        logger.error("Ошибка: callback не содержит данных.")
        return

    file_name = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id

    # URL ручки FastAPI для скачивания файла
    api_url = f"{settings.BOT_WEBHOOK_URL}/get-file"

    try:
        async with ClientSession() as session:
            async with session.get(api_url, params={"user_id": user_id, "file_name": file_name}) as response:
                if response.status == 200:
                    # Получение содержимого файла как bytes
                    file_bytes = await response.read()

                    # Создаем объект BufferedInputFile для отправки
                    input_file = BufferedInputFile(file_bytes, filename=file_name)

                    await callback.message.answer_document(
                        document=input_file,
                        caption=f"Ваш файл: {file_name}"
                    )
                    await callback.answer("Файл успешно отправлен!")
                else:
                    logger.error(f"Ошибка API: {response.status}")
                    await callback.message.answer("Ошибка при получении файла.")
    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        await callback.message.answer("Произошла ошибка при отправке файла.")
