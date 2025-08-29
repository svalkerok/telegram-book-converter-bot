"""
Модуль с inline-клавиатурами.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Set
from config import SUPPORTED_OUTPUT_FORMATS


def create_format_keyboard(
    current_format: str,
    exclude_formats: Set[str] = None
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора формата конвертации.
    
    Args:
        current_format: Текущий формат файла
        exclude_formats: Форматы для исключения
        
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками форматов
    """
    exclude = exclude_formats or {current_format}
    buttons = []
    
    for format_key, format_name in SUPPORTED_OUTPUT_FORMATS.items():
        if format_key not in exclude:
            buttons.append(
                InlineKeyboardButton(
                    text=f"📄 {format_name}",
                    callback_data=f"convert:{format_key}"
                )
            )
    
    # Группируем кнопки по 2 в ряд
    keyboard = []
    for i in range(0, len(buttons), 2):
        keyboard.append(buttons[i:i+2])
    
    # Добавляем кнопку отмены
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="cancel"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
