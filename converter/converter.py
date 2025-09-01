"""
Модуль конвертации книг между форматами.
"""
import asyncio
import subprocess
import re
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
    
    def generate_output_filename(self, input_path: Path, output_format: str) -> Path:
        """
        Генерирует имя выходного файла с улучшенной схемой именования.
        
        Args:
            input_path: Путь к исходному файлу
            output_format: Целевой формат (без точки)
            
        Returns:
            Path к выходному файлу
        """
        # Получаем имя файла без расширения
        original_name = input_path.stem
        
        # Очищаем имя файла от специальных символов
        clean_name = re.sub(r'[<>:"/\\|?*]', '', original_name)
        clean_name = re.sub(r'\s+', '_', clean_name.strip())
        
        # Ограничиваем длину имени
        if len(clean_name) > 50:
            clean_name = clean_name[:50]
        
        # Если имя пустое, используем дефолтное
        if not clean_name:
            clean_name = "Book"
        
        # Создаем новое имя файла
        new_filename = f"{clean_name}_Конвертовано.{output_format}"
        
        # Возвращаем путь в той же директории
        return input_path.parent / new_filename
        
    def get_conversion_params(self, output_format: str) -> list:
        """
        Получает специфичные параметры конвертации для формата.
        
        Args:
            output_format: Целевой формат
            
        Returns:
            Список дополнительных параметров для ebook-convert
        """
        params = ['--enable-heuristics']
        
        if output_format.lower() == 'epub':
            # Специальные параметры для EPUB, совместимые с Kindle
            params.extend([
                '--epub-version=2',           # Используем EPUB 2.0 для совместимости
                '--epub-inline-toc',          # Встроенное оглавление
                '--epub-toc-at-end',          # Оглавление в конце
                '--epub-flatten',             # Плоская структура файлов
                '--no-default-epub-cover',    # Не добавлять автообложку
                '--authors=Unknown Author',   # Автор по умолчанию
                '--title=Converted Book',     # Название по умолчанию
                '--language=ru',              # Язык
                '--publisher=Book Converter Bot',  # Издатель
                '--linearize-tables',         # Линеаризация таблиц
                '--smarten-punctuation',      # Умная пунктуация
            ])
        elif output_format.lower() == 'mobi':
            # Параметры для MOBI
            params.extend([
                '--authors=Unknown Author',
                '--title=Converted Book',
                '--language=ru',
                '--mobi-toc-at-start',
                '--mobi-ignore-margins',
            ])
        elif output_format.lower() == 'pdf':
            # Параметры для PDF
            params.extend([
                '--pdf-page-numbers',
                '--pdf-sans-family=Liberation Sans',
                '--pdf-serif-family=Liberation Serif',
                '--pdf-mono-family=Liberation Mono',
            ])
        
        return params
    
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
        # Генерируем путь для выходного файла с улучшенным именем
        output_path = self.generate_output_filename(input_path, output_format)
        
        # Получаем специфичные параметры для формата
        format_params = self.get_conversion_params(output_format)
        
        # Команда для ebook-convert
        cmd = [
            'ebook-convert',
            str(input_path),
            str(output_path)
        ] + format_params
        
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
