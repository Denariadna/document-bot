from aiogram import types
# Функция обработки команды /start
async def start(message: types.Message):
    await message.reply("Привет! Я бот, и я готов помочь!")

# Функция, которая просто повторяет сообщение пользователя
async def echo(message: types.Message):
    await message.answer(message.text)
