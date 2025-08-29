"""
Обработчик документов.
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from pathlib import Path
import logging
import io

from converter.converter import BookConverter
from converter.validators import FileValidator
from utils.file_manager import TempFileManager
from keyboards.inline import create_format_keyboard
from config import MAX_FILE_SIZE

logger = logging.getLogger(__name__)
router = Router()

file_manager = TempFileManager()
converter = BookConverter()
validator = FileValidator()


@router.message(F.document)
async def handle_document(message: Message, state: FSMContext):
    """
    Обработчик входящих документов.
    
    Args:
        message: Сообщение с документом
        state: Состояние FSM
    """
    document = message.document
    
    # Проверяем размер
    if document.file_size > MAX_FILE_SIZE:
        await message.reply(
            f"❌ Файл слишком большой!\n"
            f"Максимальный размер: {MAX_FILE_SIZE // 1_048_576} МБ"
        )
        return
    
    # Отправляем статус
    status_msg = await message.reply("⏳ Загружаю файл...")
    
    try:
        # Скачиваем файл
        file = await message.bot.get_file(document.file_id)
        file_data = await message.bot.download_file(file.file_path)
        
        # Читаем данные из BytesIO
        if isinstance(file_data, io.BytesIO):
            file_bytes = file_data.getvalue()
        else:
            file_bytes = file_data
        
        # Сохраняем во временный файл
        temp_path = await file_manager.save_file_from_bytes(
            file_bytes, 
            document.file_name
        )
        
        # Валидируем
        is_valid, error = validator.validate_file(temp_path)
        if not is_valid:
            await status_msg.edit_text(f"❌ {error}")
            # Удаляем временный файл
            try:
                temp_path.unlink()
            except:
                pass
            return
        
        # Определяем формат
        current_format = temp_path.suffix.lstrip('.')
        
        # Сохраняем путь в состоянии
        await state.update_data(
            file_path=str(temp_path),
            file_name=document.file_name,
            current_format=current_format
        )
        
        # Показываем клавиатуру с форматами
        await status_msg.edit_text(
            f"📄 Файл: *{document.file_name}*\n"
            f"📊 Формат: *{current_format.upper()}*\n"
            f"📦 Размер: *{document.file_size // 1024} КБ*\n\n"
            f"Выберите формат для конвертации:",
            parse_mode="Markdown",
            reply_markup=create_format_keyboard(current_format)
        )
        
    except Exception as e:
        logger.error(f"Ошибка обработки документа: {e}")
        await status_msg.edit_text(
            "❌ Произошла ошибка при обработке файла.\n"
            "Попробуйте еще раз."
        )
