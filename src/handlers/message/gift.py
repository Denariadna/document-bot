# import asyncio
# import json
# from typing import Any

# import aiohttp
# import aio_pika
# import msgpack
# from aio_pika import Queue
# from aio_pika.exceptions import QueueEmpty
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, InputFile, BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram import F

# from config.settings import settings
# from ..buttons import START_GIFTING


# from .router import router
# from src.handlers.states.gift import GiftGroup
# from src.storage import rabbit
# from src.templates.env import render


# # @router.message(GiftGroup.gifting)
# # async def gifting(message: Message, state: FSMContext) -> None:
# #     await message.answer('ypa')


# @router.message(F.text == START_GIFTING)
# async def start_gifting(message: Message, state: FSMContext) -> None:
#     # await state.set_state(GiftGroup.gifting)

#     async with rabbit.channel_pool.acquire() as channel:  # type: aio_pika.Channel
#         queue: Queue = await channel.declare_queue(
#             settings.USER_GIFT_QUEUE_TEMPLATE.format(user_id=message.from_user.id),
#             durable=True,
#         )

#         retries = 3
#         for _ in range(retries):
#             try:
#                 gift = await queue.get()
#                 parsed_gift: dict[str, Any] = msgpack.unpackb(gift.body)

#                 # async with aiohttp.ClientSession() as session:
#                 #     async with session.get('https://cdn.velostrana.ru/upload/models/velo/63352/full.jpg') as response:
#                 #         content = await response.read()
#                 #
#                 # photo = BufferedInputFile(content, 'test')
#                 # # callback buttons

#                 like_btn = InlineKeyboardButton(text='👍', callback_data='like')
#                 dislike_btn = InlineKeyboardButton(text='👎', callback_data='dislike')
#                 inline_btn_1 = InlineKeyboardButton(text='Следующий подарок', callback_data='next_gift')
#                 markup = InlineKeyboardMarkup(
#                     inline_keyboard=[[like_btn, dislike_btn], [inline_btn_1]]
#                 )

#                 await message.answer_photo(
#                     photo=parsed_gift['photo'],
#                     caption=render('gift/gift.jinja2', gift=parsed_gift),
#                     reply_markup=markup,
#                 )
#                 return
#             except QueueEmpty:
#                 await asyncio.sleep(1)

#         await message.answer('Нет подарков')
