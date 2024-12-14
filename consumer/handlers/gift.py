# import random

# import aio_pika
# import msgpack
# from aio_pika import ExchangeType
# from sqlalchemy import select, func

# from config.settings import settings
# from consumer.logger import correlation_id_ctx
# from consumer.model.gift import Gift
# from consumer.schema.gift import GiftMessage
# from consumer.storage import rabbit, db


# async def handle_event_gift(message: GiftMessage):
#     if message['action'] == 'get_gifts':
#         async with db.async_session() as db_session:
#             # gifts = (await db.scalars(select(Gift).order_by(func.random()))).all()

#             not_fetched = await db_session.execute(select(Gift).order_by(func.random()))
#             tuple_rows = not_fetched.all()
#             gifts = [row for row, in tuple_rows]

#             async with rabbit.channel_pool.acquire() as channel:  # type: aio_pika.Channel
#                 exchange = await channel.declare_exchange("user_gifts", ExchangeType.TOPIC, durable=True)

#                 for gift in gifts:
#                     await exchange.publish(
#                         aio_pika.Message(
#                             msgpack.packb({
#                                 'name': gift.name,
#                                 'photo': gift.photo,
#                                 'category': gift.category,
#                             }),
#                             correlation_id=correlation_id_ctx.get(),
#                         ),
#                         routing_key=settings.USER_GIFT_QUEUE_TEMPLATE.format(user_id=message['user_id']),
#                     )
