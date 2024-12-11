from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.future import select
from src.storage.minio_client import upload_file
from src.storage.db import async_session
from src.model.meta import FileRecord
from src.logger import logger  # Импорт логгера
from pathlib import Path

# Определение состояний
class UploadStates(StatesGroup):
    waiting_for_file = State()

async def upload(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        logger.error("Ошибка: сообщение не содержит информации об отправителе (from_user = None).")
        return
    user_id = message.from_user.id

    # Проверяем состояние
    current_state = await state.get_state()
    if current_state == UploadStates.waiting_for_file.state:
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
        unique_name = upload_file(user_id, document.file_name, file_bytes.read())

        # Сохраняем данные в БД
        async with async_session() as db:
            record = FileRecord(user_id=user_id, file_name=document.file_name, file_exention=Path(document.file_name).suffix, file_path=unique_name)
            db.add(record)
            await db.commit()

        # Сбрасываем состояние
        await state.clear()
        await message.reply(f"Файл {document.file_name} успешно загружен!")
    else:
        # Если состояние не установлено, устанавливаем его
        await state.set_state(UploadStates.waiting_for_file)
        await message.reply("Отправьте файл, который хотите загрузить.")

async def check_state(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await message.reply(f"Текущее состояние: {current_state or 'Нет состояния'}")

async def show_files(message: types.Message) -> None:
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    if message.from_user is None:
        logger.error("Ошибка: сообщение не содержит информации об отправителе (from_user = None).")
        return
    user_id = message.from_user.id
    async with async_session() as db:
        result = await db.execute(
            select(FileRecord.file_name).where(FileRecord.user_id == user_id)
        )
        files = result.scalars().all()

    if not files:
        await message.reply("У вас нет загруженных файлов.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=file, callback_data=f"file:{file}")]
        for file in files
    ])

    await message.reply("Ваши файлы:", reply_markup=keyboard)
