import asyncio

import msgpack
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aio_pika import Queue

from config.settings import settings
from src.storage.rabbit import channel_pool
from .router import router


async def listen(callback_query: CallbackQuery, user_id: str):
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        queue: Queue = await channel.declare_queue(settings.USER_GIFT_QUEUE_TEMPLATE.format(user_id=user_id), durable=True)
        message = await queue.get()
        parsed_message: Gift = msgpack.unpackb(message)
        await callback_query.answer(parsed_message)
#
#
# @router.callback_query()
# async def callback_test(callback_query: CallbackQuery, state: FSMContext) -> None:
#     data = await state.get_data()
#     await callback_query.answer('Hello from callback!')  # as popup
#     await callback_query.message.answer('Hello from callback!')  # as message
