import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.future import select
from consumer.handlers.show_file import show_files
from consumer.schema.file import FileMessage
from src.model.file import FileRecord


@pytest.mark.asyncio
@patch("consumer.bot.bot.send_message")
@patch("consumer.storage.db.async_session")
async def test_show_files(mock_async_session, mock_send_message):
    user_id = 123
    files = ["file1.txt", "file2.pdf"]
    message = FileMessage(user_id=user_id, action="show_files_user")

    # Мок для базы данных
    mock_session = AsyncMock()
    mock_session.execute.return_value.scalars.return_value.all.return_value = files
    mock_async_session.return_value.__aenter__.return_value = mock_session

    # Тестируем вызов функции
    await show_files(message)

    # Проверяем вызовы к базе данных
    mock_session.execute.assert_called_once_with(
        select(FileRecord.file_name).where(FileRecord.user_id == user_id)
    )

    # Проверяем отправку сообщения через Telegram-бота
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[{"text": file, "callback_data": f"file:{file}"}] for file in files]
    )
    mock_send_message.assert_called_once_with(chat_id=user_id, text="Ваши файлы:", reply_markup=keyboard)


@pytest.mark.asyncio
@patch("consumer.bot.bot.send_message")
@patch("consumer.storage.db.async_session")
async def test_show_files_no_files(mock_async_session, mock_send_message):
    user_id = 123
    message = FileMessage(user_id=user_id, action="show_files_user")

    # Мок для базы данных (пустой результат)
    mock_session = AsyncMock()
    mock_session.execute.return_value.scalars.return_value.all.return_value = []
    mock_async_session.return_value.__aenter__.return_value = mock_session

    # Тестируем вызов функции
    await show_files(message)

    # Проверяем отправку сообщения о пустых файлах
    mock_send_message.assert_called_once_with(chat_id=user_id, text="У вас нет загруженных файлов.")
