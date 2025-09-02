"""
Обработчик callback-запросов с поддержкой прогрессивной конвертации.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from pathlib import Path
import logging

from converter.converter import BookConverter
from converter.validators import FileValidator
from utils.file_manager import TempFileManager
from utils.error_manager import error_manager, ErrorCode

logger = logging.getLogger(__name__)
router = Router()

converter = BookConverter()


@router.callback_query(F.data.startswith("convert:"))
async def handle_conversion(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора формата для конвертации с прогрессивными уведомлениями.
    """
    target_format = callback.data.split(":")[1]
    
    data = await state.get_data()
    file_path = data.get("file_path")
    file_name = data.get("file_name")
    user_id = callback.from_user.id
    
    if not file_path:
        await callback.answer("❌ Файл не найден. Отправьте файл заново.")
        await callback.message.delete()
        return
    
    # Проверяем размер файла для определения стратегии
    input_path = Path(file_path)
    file_size_mb = input_path.stat().st_size / (1024 * 1024)
    
    # Начальное сообщение
    if file_size_mb > 20:
        initial_message = (
            f"🚀 *Конвертация большого файла*\n"
            f"📄 *Файл:* {file_name} ({file_size_mb:.1f} МБ)\n"
            f"🎯 *Формат:* {target_format.upper()}\n\n"
            f"⚡ *Применяется оптимизация для больших файлов*\n"
            f"⏳ *Это займет больше времени, но результат будет лучше*"
        )
    else:
        initial_message = (
            f"⏳ Конвертирую *{file_name}* в *{target_format.upper()}*...\n"
            f"Это может занять некоторое время."
        )
    
    await callback.message.edit_text(initial_message, parse_mode="Markdown")
    
    # Функция для обновления прогресса
    async def update_progress(message: str):
        try:
            current_text = (
                f"🚀 *Конвертация в процессе*\n"
                f"📄 *Файл:* {file_name}\n"
                f"🎯 *Формат:* {target_format.upper()}\n\n"
                f"{message}"
            )
            await callback.message.edit_text(current_text, parse_mode="Markdown")
        except Exception as e:
            logger.warning(f"Не удалось обновить прогресс: {e}")
    
    try:
        # Запускаем конвертацию с callback для прогресса
        output_path = await converter.convert(
            input_path, 
            target_format, 
            progress_callback=update_progress,
            user_id=user_id
        )
        
        if output_path and output_path.exists():
            # Отправляем результат
            document = FSInputFile(output_path, filename=output_path.name)
            
            output_size_mb = output_path.stat().st_size / (1024 * 1024)
            
            # Специальное сообщение для больших файлов
            if file_size_mb > 20:
                caption = (
                    f"🎉 *Большой файл успешно сконвертирован!*\n\n"
                    f"📄 *Исходный файл:* {file_name} ({file_size_mb:.1f} МБ)\n"
                    f"📊 *Результат:* {output_path.name} ({output_size_mb:.1f} МБ)\n"
                    f"🎯 *Формат:* {target_format.upper()}\n\n"
                    f"🔥 *Оптимизировано для быстрой загрузки!*"
                    + (f"\n⚡ *Совместимо с Kindle!*" if target_format.lower() == 'epub' else "")
                )
            else:
                caption = (
                    f"✅ *Готово!* Ваш файл в формате *{target_format.upper()}*\n"
                    f"📄 *Имя файла:* `{output_path.name}`\n"
                    f"📊 *Размер:* {output_size_mb:.1f} МБ\n\n"
                    + (f"🔥 *Оптимизировано для Kindle!*" if target_format.lower() == 'epub' else "")
                )
            
            await callback.message.answer_document(
                document=document,
                caption=caption,
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
            # Конвертация не удалась - используем систему ошибок
            error_id = error_manager.log_error(
                ErrorCode.CONVERSION_FAILED,
                context={
                    'target_format': target_format,
                    'file_name': file_name,
                    'file_size_mb': file_size_mb,
                    'callback_data': callback.data
                },
                user_id=user_id
            )
            
            # Специальные сообщения об ошибках для больших файлов
            if file_size_mb > 50:
                error_message = (
                    f"❌ *Не удалось конвертировать очень большой файл*\n\n"
                    f"� *Размер:* {file_size_mb:.1f} МБ (очень большой)\n\n"
                    f"�🔍 *Возможные решения:*\n"
                    f"• Разделите файл на части (по 20-30 МБ)\n"
                    f"• Уменьшите качество изображений в PDF\n"
                    f"• Попробуйте формат TXT для текстовых документов\n"
                    f"• Используйте онлайн-компрессор PDF\n\n"
                    f"🆔 *Код ошибки:* `{ErrorCode.CONVERSION_FAILED.value}` | *ID:* `{error_id}`\n"
                    f"💡 *Рекомендация:* Файлы больше 50 МБ лучше конвертировать частями"
                )
            elif file_size_mb > 20:
                error_message = (
                    f"❌ *Не удалось конвертировать большой файл*\n\n"
                    f"📊 *Размер:* {file_size_mb:.1f} МБ\n\n"
                    f"🔍 *Специфичные причины для больших файлов:*\n"
                    f"• Сложная структура документа с большим количеством изображений\n"
                    f"• Поврежденные метаданные в PDF\n"
                    f"• Нестандартное форматирование\n\n"
                    f"💡 *Попробуйте:*\n"
                    f"• Экспортировать PDF заново из источника\n"
                    f"• Конвертировать в TXT (только текст)\n"
                    f"• Разбить на несколько файлов\n"
                    f"• Уменьшить размер через PDF-компрессор\n\n"
                    f"🆔 *Код ошибки:* `{ErrorCode.CONVERSION_FAILED.value}` | *ID:* `{error_id}`"
                )
            else:
                error_message = error_manager.get_user_message(ErrorCode.CONVERSION_FAILED, error_id)
            
            await callback.message.edit_text(error_message, parse_mode="Markdown")
            
    except Exception as e:
        # Обрабатываем неожиданные ошибки
        error_id = error_manager.log_error(
            ErrorCode.UNKNOWN_ERROR,
            exception=e,
            context={
                'target_format': target_format,
                'file_name': file_name,
                'file_size_mb': file_size_mb,
                'callback_data': callback.data
            },
            user_id=user_id
        )
        
        error_message = error_manager.get_user_message(ErrorCode.UNKNOWN_ERROR, error_id)
        
        logger.error(f"Ошибка в handle_conversion: {e} (Error ID: {error_id})")
        await callback.message.edit_text(
            error_message,
            parse_mode="Markdown"
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
