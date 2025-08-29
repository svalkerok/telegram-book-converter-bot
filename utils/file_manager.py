"""
Модуль управления временными файлами.
"""
import os
import tempfile
from pathlib import Path
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aiofiles
import logging

logger = logging.getLogger(__name__)


class TempFileManager:
    """Менеджер временных файлов с автоматической очисткой."""
    
    def __init__(self, base_dir: str = "/tmp/book_converter"):
        """
        Инициализация менеджера.
        
        Args:
            base_dir: Базовая директория для временных файлов
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    @asynccontextmanager
    async def temp_file(
        self, 
        suffix: str = "",
        prefix: str = "book_"
    ) -> AsyncGenerator[Path, None]:
        """
        Контекстный менеджер для работы с временным файлом.
        
        Args:
            suffix: Суффикс файла (расширение)
            prefix: Префикс имени файла
            
        Yields:
            Path: Путь к временному файлу
        """
        # Создаем временный файл
        fd, path = tempfile.mkstemp(
            suffix=suffix,
            prefix=prefix,
            dir=self.base_dir
        )
        os.close(fd)  # Закрываем дескриптор
        
        temp_path = Path(path)
        
        try:
            yield temp_path
        finally:
            # Гарантированно удаляем файл
            try:
                if temp_path.exists():
                    temp_path.unlink()
                    logger.debug(f"Удален временный файл: {temp_path}")
            except Exception as e:
                logger.error(f"Ошибка при удалении файла {temp_path}: {e}")
                
    async def save_file_from_bytes(
        self,
        data: bytes,
        filename: str
    ) -> Path:
        """
        Сохраняет байты во временный файл.
        
        Args:
            data: Данные файла
            filename: Имя файла для определения расширения
            
        Returns:
            Path: Путь к сохраненному файлу
        """
        suffix = Path(filename).suffix
        fd, path = tempfile.mkstemp(
            suffix=suffix,
            prefix="book_",
            dir=self.base_dir
        )
        os.close(fd)
        
        temp_path = Path(path)
        async with aiofiles.open(temp_path, 'wb') as f:
            await f.write(data)
        return temp_path
