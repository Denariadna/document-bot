from aiogram import Router
from aiogram.filters import Command
from .start import start, echo, help_command
from .file import upload, download

router = Router()

# Регистрируем обработчики команд и текстовых сообщений
router.message.register(start, Command("start"))  
router.message.register(upload, Command("upload"))
router.message.register(download, Command("download"))
router.message.register(help_command, Command("help"))
router.message.register(echo)

