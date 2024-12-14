import aio_pika
from aio_pika import Channel, connect_robust
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from typing import cast

from config.settings import settings


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbit_url)

connection_pool: Pool[AbstractRobustConnection] = Pool(get_connection, max_size=2)


async def get_channel() -> Channel:
    async with connection_pool.acquire() as connection:
        return cast(Channel, await connection.channel())


channel_pool: Pool[Channel] = Pool(get_channel, max_size=10)