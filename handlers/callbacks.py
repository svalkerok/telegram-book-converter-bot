"""
Обработчик callback-запросов.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from pathlib import Path
import logging

from converter.converter import BookConverter
from converter.validators import FileValidator
from utils.file_manager import TempFileManager

logger = logging.getLogger(__name__)
router = Router()

converter = BookConverter()


@router.callback_query(F.data.startswith("convert:"))
async def handle_conversion(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора формата для конвертации.
    
    Args:
        callback: Callback query
        state: Состояние FSM
    """
    # Получаем целевой формат
    target_format = callback.data.split(":")[1]
    
    # Получаем данные из состояния
    data = await state.get_data()
    file_path = data.get("file_path")
    file_name = data.get("file_name")
    
    if not file_path:
        await callback.answer("❌ Файл не найден. Отправьте файл заново.")
        await callback.message.delete()
        return
    
    # Обновляем сообщение
    await callback.message.edit_text(
        f"⏳ Конвертирую *{file_name}* в *{target_format.upper()}*...\n"
        f"Это может занять некоторое время.",
        parse_mode="Markdown"
    )
    
    try:
        # Конвертируем
        input_path = Path(file_path)
        output_path = await converter.convert(input_path, target_format)
        
        if output_path and output_path.exists():
            # Отправляем результат
            document = FSInputFile(output_path, filename=output_path.name)
            await callback.message.answer_document(
                document=document,
                caption=f"✅ Готово! Ваш файл в формате *{target_format.upper()}*",
                parse_mode="Markdown"
            )
            
            # Удаляем сообщение со статусом
            await callback.message.delete()
            
            # Удаляем файлы
            try:
                input_path.unlink()
                output_path.unlink()
            except:
                pass
        else:
            await callback.message.edit_text(
                "❌ Не удалось конвертировать файл.\n"
                "Попробуйте другой формат или проверьте файл."
            )
            
    except Exception as e:
        logger.error(f"Ошибка конвертации: {e}")
        await callback.message.edit_text(
            "❌ Произошла ошибка при конвертации.\n"
            "Попробуйте еще раз."
        )
    finally:
        # Очищаем состояние
        await state.clear()


@router.callback_query(F.data == "cancel")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик отмены операции.
    
    Args:
        callback: Callback query
        state: Состояние FSM
    """
    await state.clear()
    await callback.message.delete()
    await callback.answer("Операция отменена")
