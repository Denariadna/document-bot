import pytest
from unittest.mock import MagicMock, patch
from consumer.handlers.show_file import show_files
from consumer.schema.file import FileMessage
from consumer.storage import db
from src.model.file import FileRecord


@pytest.mark.asyncio
async def test_show_files():
    message = FileMessage(user_id=123)

    # Мокаем доступ к базе данных
    with patch('consumer.storage.db.async_session') as mock_session:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = ['file1.txt', 'file2.txt']
        mock_session.return_value.__aenter__.return_value.execute = MagicMock(return_value=mock_result)

        # Мокаем Telegram bot
        with patch('consumer.bot.bot.send_message') as mock_send_message:
            await show_files(message)

            # Проверяем, что запрос к базе данных был выполнен
            mock_session.return_value.__aenter__.return_value.execute.assert_called_once()

            # Проверяем, что сообщение было отправлено
            mock_send_message.assert_called_once_with(
                chat_id=123, text='Ваши файлы:', reply_markup=MagicMock()
            )
