"""
Менеджер ошибок с системой нумерации для диагностики.
"""
import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ErrorCode(Enum):
    """Коды ошибок для системы диагностики."""
    
    # Ошибки конвертации (100-199)
    CONVERSION_FAILED = 101
    CONVERSION_TIMEOUT = 102
    CONVERSION_INVALID_FORMAT = 103
    CONVERSION_CORRUPTED_FILE = 104
    CONVERSION_MEMORY_ERROR = 105
    
    # Ошибки файловой системы (200-299)
    FILE_NOT_FOUND = 201
    FILE_ACCESS_DENIED = 202
    FILE_TOO_LARGE = 203
    FILE_INVALID_TYPE = 204
    
    # Ошибки валидации (300-399)
    VALIDATION_FAILED = 301
    VALIDATION_UNSUPPORTED_FORMAT = 302
    VALIDATION_EMPTY_FILE = 303
    
    # Системные ошибки (400-499)
    SYSTEM_OUT_OF_MEMORY = 401
    SYSTEM_DISK_FULL = 402
    SYSTEM_CALIBRE_ERROR = 403
    
    # Неизвестные ошибки (500-599)
    UNKNOWN_ERROR = 501


class ErrorManager:
    """Менеджер для обработки и логирования ошибок с уникальными ID."""
    
    def __init__(self):
        self.error_log: Dict[str, Dict[str, Any]] = {}
    
    def generate_error_id(self) -> str:
        """Генерирует уникальный ID ошибки."""
        return f"ERR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    def log_error(self, 
                  error_code: ErrorCode, 
                  exception: Optional[Exception] = None,
                  context: Optional[Dict[str, Any]] = None,
                  user_id: Optional[int] = None) -> str:
        """
        Логирует ошибку и возвращает уникальный ID.
        
        Args:
            error_code: Код ошибки
            exception: Исключение (если есть)
            context: Дополнительный контекст
            user_id: ID пользователя
            
        Returns:
            Уникальный ID ошибки
        """
        error_id = self.generate_error_id()
        
        error_info = {
            'error_code': error_code,
            'timestamp': datetime.now().isoformat(),
            'exception': str(exception) if exception else None,
            'exception_type': type(exception).__name__ if exception else None,
            'context': context or {},
            'user_id': user_id
        }
        
        self.error_log[error_id] = error_info
        
        # Логируем в файл
        logger.error(
            f"Error {error_id}: Code={error_code.value} ({error_code.name}), "
            f"Exception={exception}, Context={context}, User={user_id}"
        )
        
        return error_id
    
    def get_user_message(self, error_code: ErrorCode, error_id: str) -> str:
        """
        Возвращает пользовательское сообщение об ошибке.
        
        Args:
            error_code: Код ошибки
            error_id: ID ошибки
            
        Returns:
            Сообщение для пользователя
        """
        base_messages = {
            ErrorCode.CONVERSION_FAILED: {
                'title': '❌ Не удалось конвертировать файл',
                'causes': [
                    '• Файл поврежден или имеет неподдерживаемую структуру',
                    '• Недостаточно памяти для обработки',
                    '• Проблема с исходным форматом'
                ],
                'solutions': [
                    '• Выбрать другой формат для конвертации',
                    '• Проверить файл на целостность', 
                    '• Отправить файл заново'
                ]
            },
            ErrorCode.CONVERSION_TIMEOUT: {
                'title': '⏰ Таймаут конвертации',
                'causes': [
                    '• Файл слишком большой для обработки',
                    '• Сложная структура документа',
                    '• Перегрузка сервера'
                ],
                'solutions': [
                    '• Попробовать файл меньшего размера',
                    '• Повторить попытку позже',
                    '• Разбить документ на части'
                ]
            },
            ErrorCode.FILE_TOO_LARGE: {
                'title': '📦 Файл слишком большой',
                'causes': [
                    '• Размер файла превышает лимит (50 МБ)',
                    '• Файл содержит много изображений',
                    '• Несжатый формат'
                ],
                'solutions': [
                    '• Сжать файл перед отправкой',
                    '• Удалить лишние изображения',
                    '• Разделить на несколько файлов'
                ]
            },
            ErrorCode.VALIDATION_UNSUPPORTED_FORMAT: {
                'title': '🚫 Неподдерживаемый формат',
                'causes': [
                    '• Формат файла не поддерживается',
                    '• Неверное расширение файла',
                    '• Поврежденные метаданные'
                ],
                'solutions': [
                    '• Проверить список поддерживаемых форматов',
                    '• Конвертировать в поддерживаемый формат',
                    '• Исправить расширение файла'
                ]
            }
        }
        
        # Получаем сообщение или используем дефолтное
        message_data = base_messages.get(error_code, {
            'title': '❌ Произошла ошибка',
            'causes': ['• Неизвестная ошибка в системе'],
            'solutions': ['• Попробуйте позже', '• Обратитесь к администратору']
        })
        
        # Формируем итоговое сообщение
        causes_text = '\n'.join(message_data['causes'])
        solutions_text = '\n'.join(message_data['solutions'])
        
        return (
            f"{message_data['title']}\n\n"
            f"🔍 *Возможные причины:*\n{causes_text}\n\n"
            f"💡 *Попробуйте:*\n{solutions_text}\n\n"
            f"🆔 *Код ошибки:* `{error_code.value}` | *ID:* `{error_id}`\n"
            f"📞 При обращении в поддержку укажите этот код"
        )


# Глобальный экземпляр менеджера ошибок
error_manager = ErrorManager()
