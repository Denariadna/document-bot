from aiogram import types
import logging
logger = logging.getLogger(__name__)
from src.handlers.states.auth import AuthGroup
from aiogram.fsm.context import FSMContext

# Функция обработки команды /start
async def start(message: types.Message, state: FSMContext) -> None:
    await state.set_data({})
    await state.get_data()
    await state.set_state(AuthGroup.authorized)
    await state.get_state()
    await message.reply("добро пожаловать в документ-бот, возможные команды можно посмотреть по команде /help")


# функция обработки команды /help
async def help_command(message: types.Message)-> None:
    commands = (
        "/help - показать доступные команды",
        "/upload - загрузить файл",
        "/show_files - отобразить файлы",
        "/check_state - проверить состояние"
    )
    await message.reply("\n".join(commands))