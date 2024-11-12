import asyncio
import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from config.settings import settings
from src.bot import setup_bot, setup_dp
from src.handlers.command.router import router as command_router


logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting lifespan...")

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    setup_dp(dp)
    setup_bot(bot)

    # Подключаем командный роутер
    dp.include_router(command_router)

    await bot.set_webhook(settings.BOT_WEBHOOK_URL)
    yield

    await bot.delete_webhook()
    await bot.session.close()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app

async def start_polling():
    dp = Dispatcher()
    setup_dp(dp)
    bot = Bot(token=settings.BOT_TOKEN)
    setup_bot(bot)
    dp.include_router(command_router)
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    if settings.BOT_WEBHOOK_URL:
        uvicorn.run("src.app:create_app", factory=True, host="0.0.0.0", port=8000)
    else:
        asyncio.run(start_polling())  # запуск polling
