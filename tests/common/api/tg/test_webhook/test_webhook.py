from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from aiogram.types import Chat, Message, Update, User

from src import bot

BASE_DIR = Path(__file__).parent
SEED_DIR = BASE_DIR / 'seeds'
SEED_DIR1 = BASE_DIR / 'seeds1'


@pytest.mark.parametrize(
    ('expected_result',),
    [
        (
            [
                {"user_id": 1, "action": "upload_file", "file_name": "aaa.pdf"},
                {"user_id": 2, "action": "upload_file", "file_name": "bbb.pdf"}
            ],
        ),
        (
            [
                {"user_id": 1, "action": "upload_file", "file_name": "aaa.pdf"},
                {"user_id": 2, "action": "upload_file", "file_name": "bbb.pdf"}
            ],
        ),
    ],
)
@pytest.mark.asyncio()
async def test_webhook(expected_result, http_client, mock_bot_dp: AsyncMock) -> None:
    chat = Chat(id=1, type='private')
    user = User(id=1, is_bot=False, is_premium=False, last_name='test', first_name='test')
    message = Message(message_id=1, date=datetime.now(), chat=chat, from_user=user)
    update = Update(update_id=1, message=message).model_dump(mode='json')

    await http_client.post('/tg/webhook', json=update)
    mock_bot_dp.assert_has_calls([('feed_webhook_update', (bot.bot, update))])
