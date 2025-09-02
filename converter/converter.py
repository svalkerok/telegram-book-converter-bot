"""
Модуль конвертации книг между форматами.
"""
import asyncio
import subprocess
import re
from pathlib import Path
from typing import Optional
import logging
import time

from converter.large_file_converter import LargeFileConverter
from utils.error_manager import error_manager, ErrorCode

logger = logging.getLogger(__name__)


class BookConverter:
    """
    Конвертер книг с использованием calibre ebook-convert.
    """
    
    def __init__(self, timeout: int = 300):
        """
        Инициализация конвертера.
        
        Args:
            timeout: Таймаут конвертации в секундах (по умолчанию 5 минут)
        """
        self.timeout = timeout
        self.large_file_threshold = 20  # МБ - порог для больших файлов
        logger.info(f"BookConverter инициализирован с таймаутом {timeout} секунд")
    
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
        output_format: str,
        progress_callback: Optional[callable] = None,
        user_id: Optional[int] = None
    ) -> Optional[Path]:
        """
        Асинхронно конвертирует книгу в указанный формат с поддержкой больших файлов.
        
        Args:
            input_path: Путь к исходному файлу
            output_format: Целевой формат (без точки)
            progress_callback: Функция для уведомлений о прогрессе
            user_id: ID пользователя для логирования ошибок
            
        Returns:
            Path к конвертированному файлу или None при ошибке
        """
        start_time = time.time()
        
        try:
            # Проверяем существование файла
            if not input_path.exists():
                error_id = error_manager.log_error(
                    ErrorCode.FILE_NOT_FOUND,
                    context={'input_path': str(input_path)},
                    user_id=user_id
                )
                logger.error(f"Файл не найден: {input_path} (Error ID: {error_id})")
                return None
            
            # Проверяем размер файла
            file_size_mb = input_path.stat().st_size / (1024 * 1024)
            logger.info(f"Начало конвертации файла {input_path.name} ({file_size_mb:.1f} МБ) в {output_format}")
            
            # Для больших файлов используем специализированный конвертер
            if file_size_mb > self.large_file_threshold:
                logger.info(f"Большой файл ({file_size_mb:.1f} МБ), используем оптимизированный конвертер")
                
                large_converter = LargeFileConverter(progress_callback)
                return await large_converter.convert_with_progress(
                    input_path, 
                    output_format,
                    timeout=1800  # 30 минут для больших файлов
                )
            
            # Обычная конвертация для небольших файлов
            if progress_callback:
                await progress_callback(f"⚙️ Конвертирую в {output_format.upper()}...")
            
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
            
            logger.info(f"Выполнение команды: {' '.join(cmd)}")
            
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
            if process.returncode == 0:
                duration = time.time() - start_time
                output_size_mb = output_path.stat().st_size / (1024 * 1024) if output_path.exists() else 0
                
                logger.info(f"Конвертация завершена за {duration:.1f}с. Результат: {output_path.name} ({output_size_mb:.1f} МБ)")
                
                if progress_callback:
                    await progress_callback(f"✅ Готово! ({output_size_mb:.1f} МБ)")
                
                return output_path
            else:
                # Определяем тип ошибки по stderr
                stderr_text = stderr.decode('utf-8', errors='ignore').lower()
                
                if 'timeout' in stderr_text or 'time' in stderr_text:
                    error_code = ErrorCode.CONVERSION_TIMEOUT
                elif 'memory' in stderr_text or 'out of memory' in stderr_text:
                    error_code = ErrorCode.SYSTEM_OUT_OF_MEMORY
                elif 'corrupt' in stderr_text or 'invalid' in stderr_text:
                    error_code = ErrorCode.CONVERSION_CORRUPTED_FILE
                elif 'format' in stderr_text or 'unsupported' in stderr_text:
                    error_code = ErrorCode.CONVERSION_INVALID_FORMAT
                else:
                    error_code = ErrorCode.CONVERSION_FAILED
                
                error_id = error_manager.log_error(
                    error_code,
                    context={
                        'returncode': process.returncode,
                        'stderr': stderr_text[:500],  # Первые 500 символов
                        'command': ' '.join(cmd)
                    },
                    user_id=user_id
                )
                
                logger.error(f"Ошибка конвертации (код {process.returncode}): {stderr_text} (Error ID: {error_id})")
                return None
                
        except asyncio.TimeoutError:
            error_id = error_manager.log_error(
                ErrorCode.CONVERSION_TIMEOUT,
                context={
                    'timeout_seconds': self.timeout,
                    'file_size_mb': file_size_mb,
                    'target_format': output_format
                },
                user_id=user_id
            )
            
            logger.error(f"Таймаут конвертации ({self.timeout}s) для файла {input_path.name} (Error ID: {error_id})")
            return None
            
        except Exception as e:
            error_id = error_manager.log_error(
                ErrorCode.UNKNOWN_ERROR,
                exception=e,
                context={
                    'input_path': str(input_path),
                    'target_format': output_format,
                    'file_size_mb': file_size_mb if 'file_size_mb' in locals() else 'unknown'
                },
                user_id=user_id
            )
            
            logger.error(f"Неожиданная ошибка при конвертации: {e} (Error ID: {error_id})")
            return None
