"""
Production конфигурация для развертывания на сервере.
"""
import os
from typing import List

# Настройки для продакшена
PRODUCTION = True

# Основные настройки бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Создаем директорию для логов
import pathlib
LOG_DIR = pathlib.Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Файл логов
LOG_FILE = LOG_DIR / "bot.log"

# Настройки файлов
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
TEMP_DIR = pathlib.Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

# Поддерживаемые форматы (расширенный список для продакшена)
SUPPORTED_INPUT_FORMATS: List[str] = [
    "epub", "pdf", "mobi", "azw", "azw3", "azw4", "azw8",
    "fb2", "fbz", "txt", "html", "htm", "xhtml", "rtf",
    "doc", "docx", "odt", "pdb", "pml", "rb", "snb",
    "tcr", "txtz", "lit", "lrf", "lrx"
]

SUPPORTED_OUTPUT_FORMATS: List[str] = [
    "epub", "pdf", "mobi", "azw3", "fb2", "txt", "html",
    "rtf", "docx", "odt"
]

# Таймауты
CONVERSION_TIMEOUT = 300  # 5 минут
DOWNLOAD_TIMEOUT = 60     # 1 минута

# Настройки безопасности
ALLOWED_EXTENSIONS = SUPPORTED_INPUT_FORMATS + ['zip', 'rar']
SCAN_FILES = True  # Включить сканирование файлов на вирусы (если доступно)

# Webhook настройки (если используются)
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8000"))
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST else None

# Настройки мониторинга
HEALTH_CHECK_PORT = int(os.getenv("HEALTH_CHECK_PORT", "8080"))

# Ограничения пользователей (анти-спам)
USER_RATE_LIMIT = 10  # файлов в час на пользователя
GLOBAL_RATE_LIMIT = 100  # файлов в час глобально
