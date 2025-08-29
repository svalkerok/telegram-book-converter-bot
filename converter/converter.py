"""
Модуль конвертации книг между форматами.
"""
import asyncio
import subprocess
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BookConverter:
    """
    Конвертер книг с использованием calibre ebook-convert.
    """
    
    def __init__(self, timeout: int = 60):
        """
        Инициализация конвертера.
        
        Args:
            timeout: Таймаут конвертации в секундах
        """
        self.timeout = timeout
        
    async def convert(
        self, 
        input_path: Path, 
        output_format: str
    ) -> Optional[Path]:
        """
        Асинхронно конвертирует книгу в указанный формат.
        
        Args:
            input_path: Путь к исходному файлу
            output_format: Целевой формат (без точки)
            
        Returns:
            Path к конвертированному файлу или None при ошибке
        """
        # Генерируем путь для выходного файла
        output_path = input_path.with_suffix(f'.{output_format}')
        
        # Команда для ebook-convert
        cmd = [
            'ebook-convert',
            str(input_path),
            str(output_path),
            '--enable-heuristics'
        ]
        
        try:
            # Запускаем процесс асинхронно
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Ждем завершения с таймаутом
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )
            
            # Проверяем код возврата
            if process.returncode != 0:
                logger.error(f"Ошибка конвертации: {stderr.decode()}")
                return None
                
            # Проверяем, что файл создан
            if output_path.exists():
                return output_path
            else:
                logger.error("Выходной файл не создан")
                return None
                
        except asyncio.TimeoutError:
            logger.error("Таймаут конвертации")
            if process:
                process.kill()
            return None
        except Exception as e:
            logger.error(f"Ошибка при конвертации: {e}")
            return None
