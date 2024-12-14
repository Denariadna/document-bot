from aiogram import types
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext
from aiogram import F
from src.storage.minio_client import upload_file
from src.storage.db import async_session
from src.model.file import FileRecord
from src.logger import logger  # Импорт логгера
from pathlib import Path
from src.handlers.states.file import FileStates

from .router import router

@router.message(F.content_type == ContentType.DOCUMENT)
async def handle_file_upload(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает файл, если состояние пользователя ожидает файл.
    """

    # Проверяем текущее состояние пользователя
    current_state = await state.get_state()

    if current_state == FileStates.waiting_for_file.state:
        if message.from_user is None:
            logger.error("Ошибка: сообщение не содержит информации об отправителе (from_user = None).")
            return

        # Если ожидается файл
        if not message.document:
            await message.reply("Пожалуйста, отправьте файл.")
            return

        from src.bot import bot

        document = message.document
        file_info = await bot.get_file(document.file_id)

        if file_info.file_path is None or document.file_name is None:
            logger.error("Ошибка: не удалось получить информацию о файле. ID файла: %s", document.file_id)
            return

        file_bytes = await bot.download_file(file_info.file_path)

        if file_bytes is None:
            logger.error("Ошибка: не удалось скачать файл. ID файла: %s", document.file_id)
            return

        user_id = message.from_user.id
        unique_name = upload_file(user_id, document.file_name, file_bytes.read())

        # Сохраняем данные в БД
        async with async_session() as db:
            record = FileRecord(
                user_id=user_id,
                file_name=document.file_name,
                file_exention=Path(document.file_name).suffix,
                file_path=unique_name
            )
            db.add(record)
            await db.commit()

        # Сбрасываем состояние
        await state.clear()
        await message.reply(f"Файл {document.file_name} успешно загружен!")
    else:
        await message.reply("Ваш запрос некорректен. Используйте команду для загрузки файла.")
