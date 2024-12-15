import aio_pika
import msgpack
from aio_pika import ExchangeType
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from starlette_context import context
from starlette_context.header_keys import HeaderKeys

from src.handlers.states.file import FileStates
from src.logger import logger  # Импорт логгера
from src.schema.file import FileMessage
from src.storage.minio_client import upload_file
from src.storage.rabbit import channel_pool

from .router import router


@router.message(F.content_type == ContentType.DOCUMENT)
async def handle_file_upload(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает файл, если состояние пользователя ожидает файл.
    """

    # Проверяем текущее состояние пользователя
    current_state = await state.get_state()

    if current_state == FileStates.waiting_for_file.state:
        if message.from_user is None:
            logger.error('Ошибка: сообщение не содержит информации об отправителе (from_user = None).')
            return

        # Если ожидается файл
        if not message.document:
            await message.reply('Пожалуйста, отправьте файл.')
            return

        from src.bot import bot

        document = message.document
        file_info = await bot.get_file(document.file_id)

        if file_info.file_path is None or document.file_name is None:
            logger.error('Ошибка: не удалось получить информацию о файле. ID файла: %s', document.file_id)
            return

        file_bytes = await bot.download_file(file_info.file_path)

        if file_bytes is None:
            logger.error('Ошибка: не удалось скачать файл. ID файла: %s', document.file_id)
            return

        user_id = message.from_user.id
        unique_name = upload_file(user_id, document.file_name, file_bytes.read())

        logger.info(
            "Файл {} загружен".format(document.file_name)
            + "ID пользователя: {}".format(user_id)
            + "Путь к файлу: {}".format(unique_name)
        )

        # Подключаемся к очереди
        async with channel_pool.acquire() as channel:
            # Объявляем обменник и очередь
            exchange = await channel.declare_exchange('user_files', ExchangeType.TOPIC, durable=True)
            queue = await channel.declare_queue('user_messages', durable=True)
            await queue.bind(exchange, 'user_messages')

            await exchange.publish(
                aio_pika.Message(
                    msgpack.packb(
                        FileMessage(
                            user_id=message.from_user.id,
                            action='upload_file',
                            file_name=document.file_name,
                        ).model_dump()
                    ),
                    correlation_id=context.get(HeaderKeys.correlation_id),
                ),
                routing_key='user_messages',
            )

        # Сбрасываем состояние
        await state.clear()
        await message.reply(f'Файл {document.file_name} успешно загружен!')
    else:
        await message.reply('Ваш запрос некорректен. Используйте команду для загрузки файла.')
