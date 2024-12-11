from aiogram import Router
from aiogram.filters import Command
from .start import start, echo, help_command
from .file import upload, show_files, check_state

router = Router()

# Регистрируем обработчики команд и текстовых сообщений
router.message.register(start, Command("start"))
router.message.register(upload, Command("upload"))
router.message.register(show_files, Command("show_files"))
router.message.register(check_state, Command("check_state"))
router.message.register(help_command, Command("help"))
# router.message.register(echo)
