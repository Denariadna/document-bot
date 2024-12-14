from aiogram import types
from aiogram.fsm.context import FSMContext
import msgpack
import aio_pika
from aio_pika import ExchangeType
from src.schema.file import FileMessage
from src.storage.rabbit import channel_pool
from src.logger import logger  # Импорт логгера
from src.handlers.states.file import FileStates
from consumer.logger import correlation_id_ctx

async def initiate_upload(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        logger.error("Ошибка: сообщение не содержит информации об отправителе (from_user = None).")
        return

    # Устанавливаем состояние через FSMContext
    await state.set_state(FileStates.waiting_for_file)
    await message.reply("Отправьте файл, который хотите загрузить.")


async def check_state(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await message.reply(f"Текущее состояние: {current_state or 'Нет состояния'}")

async def show_files(message: types.Message) -> None:
    """Кладёт информацию о пользователе в очередь."""
    if message.from_user is None:
        logger.error("Ошибка: сообщение не содержит информации об отправителе (from_user = None).")
        return

    # Подключаемся к очереди через пул каналов
    async with channel_pool.acquire() as channel:
        # Объявляем обменник и очередь
        exchange = await channel.declare_exchange("user_gifts", ExchangeType.TOPIC, durable=True)
        queue = await channel.declare_queue('user_messages', durable=True)
        await queue.bind(exchange, 'user_messages')

        await exchange.publish(
            aio_pika.Message( 
                msgpack.packb(FileMessage(
                    user_id=message.from_user.id,
                    action="show_files_user"
                ).model_dump()
            ),
                # correlation_id=correlation_id_ctx.get(),
            ),
            
            routing_key='user_messages'
        )

    # Подтверждение пользователю
    await message.reply("Ваш запрос обрабатывается.")