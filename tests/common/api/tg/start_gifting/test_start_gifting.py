from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from pathlib import Path

from aiogram.types import Message, User, Chat, InlineKeyboardButton, InlineKeyboardMarkup

from src.handlers.message.gift import start_gifting
from src.templates.env import render
from tests.mocking.tg import MockTgMessage

BASE_DIR = Path(__file__).parent
SEED_DIR = BASE_DIR / 'seeds'
SEED_DIR1 = BASE_DIR / 'seeds1'


@pytest.mark.parametrize(
    ('predefined_queue',),
    [
        (
            {'photo': 'photo', 'name': 'name', 'category': 'category'},
        ),
        (
            None,
        ),
    ]
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_load_queue')
async def test_start_gifting(predefined_queue) -> None:
    user = User(id=1, is_bot=False, is_premium=False, last_name='test', first_name='test')
    message = MockTgMessage(from_user=user)

    await start_gifting(message, state=1)

    like_btn = InlineKeyboardButton(text='👍', callback_data='like')
    dislike_btn = InlineKeyboardButton(text='👎', callback_data='dislike')
    inline_btn_1 = InlineKeyboardButton(text='Следующий подарок', callback_data='next_gift')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[like_btn, dislike_btn], [inline_btn_1]]
    )
    if predefined_queue:
        message.assert_has_calls([
            ('answer_photo', {'photo': predefined_queue['photo'], 'caption': render('gift/gift.jinja2', gift=predefined_queue), 'reply_markup': markup})
        ])
    else:
        message.assert_has_calls([
            ('answer', ('Нет подарков',))
        ])
