"""
Telegram бот для конвертации электронных книг.
Точка входа приложения.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import commands, documents, callbacks

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """
    Основная функция запуска бота.
    """
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в переменных окружения")
        return
        
    # Инициализация бота и диспетчера
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация роутеров
    dp.include_router(commands.router)
    dp.include_router(documents.router)
    dp.include_router(callbacks.router)
    
    # Удаление вебхука (на случай, если был установлен)
    await bot.delete_webhook(drop_pending_updates=True)
    
    logger.info("Бот запущен")
    
    try:
        # Запуск поллинга
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
