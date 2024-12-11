from aiogram import types
import logging
logger = logging.getLogger(__name__)

# Функция обработки команды /start
async def start(message: types.Message) -> None:
    await message.reply("Урааааааа")

# функция обработки команды /help
async def help_command(message: types.Message)-> None:
    commands = (
        "/start - начать работу с ботом",
        "/help - показать доступные команды",
        "/upload - загрузить файл",
        "/show_files - скачать файл",
        "/check_state - проверить состояние"
    )
    await message.reply("\n".join(commands))

# Функция, которая просто повторяет сообщение пользователя
async def echo(message: types.Message) -> None:
    logger.info(f"Получено сообщение: {message.text}")
    if message.text:
        await message.answer(message.text)
    else:
        logger.warning("Сообщение не содержит текста.")
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")



# import aio_pika
# import msgpack
# from aio_pika import ExchangeType
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, \
#     InlineKeyboardMarkup

# from config.settings import settings
# from src.schema.gift import GiftMessage
# from .router import router
# from src.handlers.states.auth import AuthGroup
# from ..buttons import START_GIFTING
# from ...storage.rabbit import channel_pool

# # Note: Пример со стейтами
# # @router.message(Command('start'), AuthGroup.no_authorized)
# # async def start_cmd(message: Message, state: FSMContext) -> None:
# #     await state.set_state(AuthGroup.authorized)
# #     await message.answer("no_auth")
# #
# #
# # @router.message(Command('start'), AuthGroup.authorized)
# # async def start_cmd(message: Message, state: FSMContext) -> None:
# #     await state.set_state(AuthGroup.no_authorized)
# #     await message.answer("auth")


# @router.message(Command('start'))
# async def start_cmd(message: Message, state: FSMContext) -> None:
#     await state.set_data({})
#     await state.get_data()

#     await state.set_state(AuthGroup.authorized)
#     await state.get_state()
#     async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
#         exchange = await channel.declare_exchange("user_gifts", ExchangeType.TOPIC, durable=True)

#         queue = await channel.declare_queue(
#             settings.USER_GIFT_QUEUE_TEMPLATE.format(
#                 user_id=message.from_user.id,
#             ),
#             durable=True,
#         )

#         users_queue = await channel.declare_queue(
#             'user_messages',
#             durable=True,
#         )

#         # Binding queue
#         await queue.bind(
#             exchange,
#             settings.USER_GIFT_QUEUE_TEMPLATE.format(
#                 user_id=message.from_user.id,
#             ),
#         )
#         # Binding queue
#         await users_queue.bind(
#             exchange,
#             'user_messages'
#         )

#         await exchange.publish(
#             aio_pika.Message(
#                 msgpack.packb(
#                     GiftMessage(
#                         user_id=message.from_user.id,
#                         action='get_gifts',
#                         event='gift'
#                     )
#                 ),
#                 # correlation_id=context.get(HeaderKeys.correlation_id)
#             )
#             ,
#             'user_messages'
#         )


#     # await state.set_data({
#     #     'button1': 1,
#     #     'button2': 1,
#     # })

#     # # callback buttons
#     # inline_btn_1 = InlineKeyboardButton(text='Первая кнопка!', callback_data='button1')
#     # inline_btn_2 = InlineKeyboardButton(text='Вторая кнопка!', callback_data='button2')
#     # markup = InlineKeyboardMarkup(
#     #     inline_keyboard=[[inline_btn_1, inline_btn_2]]
#     # )

#     button = KeyboardButton(text=START_GIFTING)
#     markup = ReplyKeyboardMarkup(keyboard=[[button]])

#     await message.answer('Hello!', reply_markup=markup)
