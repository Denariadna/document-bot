import logging.config

import aio_pika
import msgpack

from consumer.handlers.gift import handle_event_gift
from consumer.logger import LOGGING_CONFIG, logger, correlation_id_ctx
from consumer.metrics import TOTAL_RECEIVED_MESSAGES
from consumer.schema.gift import GiftMessage
from consumer.storage import rabbit


async def start_consumer() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info('Starting consumer...')

    queue_name = "test_queue"
    async with rabbit.channel_pool.acquire() as channel:  # type: aio_pika.Channel

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10) # TODO почитать

        # Declaring queue
        queue = await channel.declare_queue(queue_name, durable=True)

        logger.info('Consumer started!')
        async with queue.iterator() as queue_iter:
            async for message in queue_iter: # type: aio_pika.Message
                TOTAL_RECEIVED_MESSAGES.inc()
                async with message.process():  # после выхода из with будет ack (есть еще no_ack)
                    correlation_id_ctx.set(message.correlation_id)

                    body: GiftMessage = msgpack.unpackb(message.body)
                    logger.info("Message: %s", body)

                    if body.get('event') == 'gift':
                        await handle_event_gift(body)


# Возможно более понятный код вида консмура
# queue: Queue
# while True:
#     message = await queue.get()
#     async with message.process():  # после выхода из with будет ack (есть еще no_ack)
#         correlation_id_ctx.set(message.correlation_id)
#         logger.info("Message ...")
#
#         body: GiftMessage = msgpack.unpackb(message.body)
#         if body['event'] == 'gift':
#             await handle_event_gift(body)
