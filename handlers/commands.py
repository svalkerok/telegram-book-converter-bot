"""
Обработчики команд бота.
"""
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import MAX_FILE_SIZE

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start.
    
    Args:
        message: Входящее сообщение
    """
    await message.answer(
        "📚 Привет! Я конвертирую книги между форматами.\n\n"
        "Просто отправь мне файл книги (PDF, EPUB, FB2, TXT, HTML), "
        "и я конвертирую его в нужный формат.\n\n"
        f"📌 Максимальный размер файла: {MAX_FILE_SIZE // 1_048_576} МБ"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Обработчик команды /help.
    
    Args:
        message: Входящее сообщение
    """
    await message.answer(
        "📖 Справка по боту\n\n"
        "Поддерживаемые форматы:\n"
        "📥 Входные: PDF, EPUB, FB2, TXT, HTML\n"
        "📤 Выходные: PDF, EPUB, FB2, TXT, HTML, MOBI\n\n"
        "⚙️ Как использовать:\n"
        "1. Отправьте файл книги\n"
        "2. Выберите формат для конвертации\n"
        "3. Получите конвертированный файл\n\n"
        "⚠️ Ограничения:\n"
        f"• Максимальный размер: {MAX_FILE_SIZE // 1_048_576} МБ\n"
        "• Время конвертации: до 60 секунд"
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    """
    Обработчик команды /cancel.
    
    Args:
        message: Входящее сообщение
    """
    await message.answer("Текущая операция отменена.")
