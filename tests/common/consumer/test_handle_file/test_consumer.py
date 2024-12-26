import pytest
from unittest.mock import MagicMock, patch
import msgpack
from consumer.app import start_consumer
from consumer.schema.file import FileMessage
from consumer.handlers.show_file import show_files
from consumer.metrics import TOTAL_RECEIVED_MESSAGES


@pytest.mark.asyncio
async def test_start_consumer():
    # Создаем mock-объект для сообщения
    mock_message = MagicMock()
    mock_message.process = MagicMock()
    mock_message.correlation_id = 'some_correlation_id'
    mock_message.body = msgpack.packb({
        'action': 'show_files_user',
        'user_id': 123
    })

    # Мокаем работу с RabbitMQ
    with patch.object(rabbit.channel_pool, 'acquire', return_value=MagicMock()) as mock_channel:
        mock_channel.return_value.__aenter__.return_value.set_qos = MagicMock()
        mock_channel.return_value.__aenter__.return_value.declare_queue = MagicMock()
        mock_channel.return_value.__aenter__.return_value.iterator = MagicMock()
        mock_channel.return_value.__aenter__.return_value.iterator.__aiter__.return_value = [mock_message]

        # Мокаем функцию show_files
        with patch('consumer.handlers.show_file.show_files', return_value=None) as mock_show_files:
            await start_consumer()
            mock_show_files.assert_called_once_with(FileMessage.model_validate(msgpack.unpackb(mock_message.body)))
