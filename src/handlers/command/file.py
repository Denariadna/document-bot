from aiogram import types
from src.storage.minio_client import upload_file, get_file_path
from src.storage.db import async_session
from src.model.meta import FileRecord

async def upload(message: types.Message) -> None:
    from src.bot import bot  # Отложенный импорт экземпляра бота

    if not message.document:
        await message.reply("Пожалуйста, отправьте файл.")
        return

    document = message.document
    file_info = await bot.get_file(document.file_id)  # Получаем информацию о файле
    file_bytes = await bot.download_file(str(file_info.file_path))  # Скачиваем файл

    if message.from_user is not None:
        user_id = message.from_user.id
    else:
        raise ValueError("user_id is None, cannot upload file")

    if document.file_name is None:
        file_name = "unknown_file_name"  # Обработка случая отсутствия имени файла
    else:
        file_name = document.file_name

    if file_bytes is None:
        raise ValueError("file_bytes is None, cannot read file content")

    # Безопасный вызов функции upload_file
    unique_name = upload_file(user_id, file_name, file_bytes.read())

    # Сохраняем данные в PostgreSQL
    async with async_session() as db:
        record = FileRecord(user_id=user_id, file_name=document.file_name, file_path=unique_name)
        db.add(record)
        await db.commit()

    await message.reply(f"Файл загружен: {unique_name}")
