from aiogram import Bot, Dispatcher
from config.settings import settings

import asyncio
from aiogram.types import Message
from aiogram.filters import Command  
from src.handlers.command.start import start as start_handler

# создаем экземпляр бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# регистрация функций
dp.message.register(start_handler, Command("start"))  # Используем фильтр Command для команды /start

# функция запуска бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

# запуск через asyncio
if __name__ == '__main__':
    asyncio.run(main())
