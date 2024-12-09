from aiogram import Router
from aiogram.filters import Command
from .start import start, echo, help_command

router = Router()

# Регистрируем обработчики команд и текстовых сообщений
router.message.register(start, Command("start"))  
router.message.register(help_command, Command("help"))
router.message.register(echo)

