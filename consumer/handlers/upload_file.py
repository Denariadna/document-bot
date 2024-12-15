from pathlib import Path

from consumer.logger import logger
from consumer.schema.file import FileMessage
from src.model.file import FileRecord
from src.storage.db import async_session


async def upload_file_handler(body: FileMessage) -> None:
    """Обрабатывает сообщение от RabbitMQ и сохраняет запись в PostgreSQL."""

    try:
        user_id = body['user_id']
        file_name = body['file_name']
        file_path = f'{user_id}_{file_name}'

        # Сохраняем запись в БД
        async with async_session() as db:
            record = FileRecord(
                user_id=user_id,
                file_name=file_name,
                file_exention=Path(file_name).suffix,
                file_path=file_path,  # Полученный путь
            )
            db.add(record)
            await db.commit()

        logger.info(f'Запись для файла {file_name} успешно добавлена в БД для пользователя {user_id}.')
    except Exception as e:
        logger.error(f'Ошибка при обработке файла в консюмере: {e}')
