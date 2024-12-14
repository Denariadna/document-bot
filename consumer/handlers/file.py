from sqlalchemy.future import select
from src.model.file import FileRecord
from src.logger import logger  # Импорт логгера

from consumer.schema.file import FileMessage
from consumer.storage import db

from consumer.bot import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def show_files(message: FileMessage) -> None:
    """Обработчик действия show_files_user."""
    # if message.from_user is None:
    #     logger.error("Message has no user information.")
    #     return
    if not message:
        logger.error("Message is not an instance of FileMessage: %s", message)
        return

    logger.info(message)

    user_id = message['user_id']

    logger.info("User ID: %s", user_id)

    # Получение списка файлов из базы данных
    async with db.async_session() as session:
        result = await session.execute(
            select(FileRecord.file_name).where(FileRecord.user_id == user_id)
        )
        logger.info("Files for user %s: %s", user_id, result)
        files = result.scalars().all()

    logger.info("Files for user %s: %s", user_id, files)

    # Отправка сообщения через Telegram-бота
    if not files:
        await bot.send_message(chat_id=user_id, text="У вас нет загруженных файлов.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=file, callback_data=f"file:{file}")]
            for file in files
        ]
    )
    logger.debug("Sending message to user_id=%s with files: %s", user_id, files, keyboard)

    await bot.send_message(chat_id=user_id, text="Ваши файлы:", reply_markup=keyboard)