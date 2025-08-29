"""
Модуль валидации входящих файлов.
"""
from pathlib import Path
from typing import Optional
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
from config import SUPPORTED_INPUT_FORMATS, MAX_FILE_SIZE, MIME_TYPES


class FileValidator:
    """Класс для валидации файлов книг."""
    
    @staticmethod
    def validate_file(file_path: Path) -> tuple[bool, Optional[str]]:
        """
        Валидирует файл книги.
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Проверка существования
        if not file_path.exists():
            return False, "Файл не найден"
            
        # Проверка размера
        if file_path.stat().st_size > MAX_FILE_SIZE:
            return False, f"Файл слишком большой (макс. {MAX_FILE_SIZE // 1_048_576} МБ)"
            
        # Проверка формата по расширению
        extension = file_path.suffix.lower().lstrip('.')
        if extension not in SUPPORTED_INPUT_FORMATS:
            return False, f"Формат .{extension} не поддерживается"
            
        # Проверка MIME-типа (если доступен python-magic)
        if MAGIC_AVAILABLE:
            try:
                mime = magic.from_file(str(file_path), mime=True)
                if mime not in MIME_TYPES:
                    return False, "Неверный тип файла"
            except Exception:
                pass  # Игнорируем ошибки magic
            
        return True, None
