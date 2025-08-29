"""
Конфигурация бота и константы.
"""
import os
from typing import Final
from dotenv import load_dotenv

# Загружаем .env только в режиме разработки
if not os.getenv("PRODUCTION"):
    load_dotenv()

# Telegram
BOT_TOKEN: Final = os.getenv("BOT_TOKEN")

# Проверка токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required. Set it in .env file or environment variable.")

# Файлы
MAX_FILE_SIZE: Final = 52_428_800  # 50 МБ в байтах
TEMP_DIR: Final = os.getenv("TEMP_DIR", "/tmp/book_converter")
CONVERSION_TIMEOUT: Final = int(os.getenv("CONVERSION_TIMEOUT", "60"))  # секунд

# Режим работы
PRODUCTION: Final = bool(os.getenv("PRODUCTION", False))
LOG_LEVEL: Final = os.getenv("LOG_LEVEL", "INFO")

# Поддерживаемые форматы
SUPPORTED_INPUT_FORMATS: Final = {
    'pdf', 'epub', 'fb2', 'txt', 'html'
}

SUPPORTED_OUTPUT_FORMATS: Final = {
    'pdf': 'PDF',
    'epub': 'EPUB', 
    'fb2': 'FB2',
    'txt': 'TXT',
    'html': 'HTML',
    'mobi': 'MOBI'
}

# MIME типы для валидации
MIME_TYPES: Final = {
    'application/pdf': 'pdf',
    'application/epub+zip': 'epub',
    'application/x-fictionbook+xml': 'fb2',
    'text/plain': 'txt',
    'text/html': 'html'
}
