from aiogram import types
from sqlalchemy.future import select
from src.storage.db import async_session
from src.model.file import FileRecord
from src.logger import logger  # Импорт логгера


async def show_files(message: types.Message) -> None:
    """Показать файлы пользователя."""
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

    logger.info("Пользователь загрузил следующие файлы: %s", files)

    if not files:
        await message.reply("У вас нет загруженных файлов.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=file, callback_data=f"file:{file}")]
            for file in files
        ]
    )
    
    await message.reply("Ваши файлы:", reply_markup=keyboard)