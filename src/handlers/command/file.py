from aiogram import types
from aiogram.types import FSInputFile
from src.storage.minio_client import upload_file, get_file_path
from src.storage.db import SessionLocal
from src.model.file import FileRecord

async def upload(message: types.Message) -> None:
    if not message.document:
        await message.reply("Пожалуйста, отправьте файл.")
        return

    document = message.document
    file_data = await document.download()
    file_bytes = file_data.read()
    user_id = message.from_user.id

    unique_name = upload_file(user_id, document.file_name, file_bytes)

    # Сохраняем данные в PostgreSQL
    db = SessionLocal()
    record = FileRecord(user_id=user_id, file_name=document.file_name, file_path=unique_name)
    db.add(record)
    db.commit()

    await message.reply(f"Файл загружен: {unique_name}")

async def download(message: types.Message) -> None:
    db = SessionLocal()
    file_name = message.text.split(maxsplit=1)[1]

    record = db.query(FileRecord).filter(FileRecord.file_path == file_name).first()
    if not record:
        await message.reply("Файл не найден.")
        return

    file_path = get_file_path(record.file_path)
    await message.reply_document(FSInputFile(file_path))
