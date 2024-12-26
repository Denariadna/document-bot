from unittest.mock import patch

import msgpack
import pytest

from consumer.app import start_consumer
from consumer.schema.file import FileMessage
from tests.mocking.rabbit import MockMessage


@pytest.mark.asyncio
async def test_start_consumer() -> None:
    # Мокаем функцию show_files
    with patch('consumer.handlers.show_file.show_files', return_value=None) as mock_show_files:
        await start_consumer()
        mock_show_files.assert_called_once_with(FileMessage.model_validate(msgpack.unpackb(MockMessage.body)))
