"""
Специализированный конвертер для больших файлов с оптимизацией и прогрессом.
"""
import asyncio
import subprocess
import logging
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import time
import os
import tempfile

logger = logging.getLogger(__name__)


class LargeFileConverter:
    """Конвертер с оптимизацией для больших файлов."""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """
        Инициализация конвертера для больших файлов.
        
        Args:
            progress_callback: Функция для уведомлений о прогрессе
        """
        self.progress_callback = progress_callback
        
    async def optimize_pdf_before_conversion(self, input_path: Path) -> Path:
        """
        Предварительная оптимизация PDF для ускорения конвертации.
        
        Args:
            input_path: Путь к исходному PDF
            
        Returns:
            Путь к оптимизированному PDF
        """
        if self.progress_callback:
            await self.progress_callback("📊 Оптимизация PDF файла...")
        
        # Создаем временный файл для оптимизированной версии
        temp_dir = Path(tempfile.gettempdir())
        optimized_path = temp_dir / f"optimized_{input_path.name}"
        
        try:
            # Команда для оптимизации PDF (удаление метаданных, сжатие)
            optimize_cmd = [
                'gs',  # Ghostscript
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                '-dPDFSETTINGS=/ebook',  # Оптимизация для электронных книг
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                '-dDetectDuplicateImages=true',
                '-dCompressFonts=true',
                '-r150',  # Понижаем разрешение до 150 DPI
                f'-sOutputFile={optimized_path}',
                str(input_path)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *optimize_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)
            
            if process.returncode == 0 and optimized_path.exists():
                original_size = input_path.stat().st_size / (1024 * 1024)
                optimized_size = optimized_path.stat().st_size / (1024 * 1024)
                
                logger.info(f"PDF оптимизирован: {original_size:.1f}MB → {optimized_size:.1f}MB")
                
                if self.progress_callback:
                    await self.progress_callback(
                        f"✅ PDF оптимизирован: {original_size:.1f}MB → {optimized_size:.1f}MB"
                    )
                
                return optimized_path
            else:
                logger.warning("Не удалось оптимизировать PDF, используем оригинал")
                if optimized_path.exists():
                    optimized_path.unlink()
                return input_path
                
        except Exception as e:
            logger.error(f"Ошибка оптимизации PDF: {e}")
            if optimized_path.exists():
                optimized_path.unlink()
            return input_path
    
    def get_optimized_conversion_params(self, target_format: str, file_size_mb: float) -> list:
        """
        Получает оптимизированные параметры конвертации для больших файлов.
        
        Args:
            target_format: Целевой формат
            file_size_mb: Размер файла в МБ
            
        Returns:
            Список параметров для ebook-convert
        """
        base_params = []
        
        # Общие оптимизации для больших файлов
        if file_size_mb > 10:  # Для файлов больше 10 МБ
            base_params.extend([
                '--max-levels=5',  # Ограничиваем глубину структуры
                '--chapter-mark=none',  # Отключаем автоматические главы
                '--page-breaks-before=/',  # Минимум разрывов страниц
                '--remove-paragraph-spacing',  # Убираем лишние отступы
                '--linearize-tables',  # Упрощаем таблицы
            ])
        
        # Специфичные для формата оптимизации
        if target_format.lower() == 'epub':
            params = base_params + [
                '--epub-version=2',
                '--epub-flatten',
                '--no-default-epub-cover',
                '--disable-font-rescaling',
                '--embed-font-family=""',  # Не встраиваем шрифты
                '--subset-embedded-fonts',
                '--smarten-punctuation',
            ]
            
            # Для очень больших файлов - агрессивная оптимизация
            if file_size_mb > 50:
                params.extend([
                    '--max-toc-links=50',  # Ограничиваем оглавление
                    '--duplicate-links-in-toc',
                    '--toc-threshold=6',
                ])
                
        elif target_format.lower() == 'mobi':
            params = base_params + [
                '--mobi-file-type=both',
                '--mobi-ignore-margins',
                '--mobi-keep-original-images=false',  # Сжимаем изображения
            ]
            
        elif target_format.lower() == 'txt':
            params = base_params + [
                '--formatting-type=plain',
                '--preserve-cover-aspect-ratio=false',
                '--txt-output-encoding=utf-8',
            ]
        else:
            params = base_params
            
        return params
    
    async def convert_with_progress(self, 
                                  input_path: Path, 
                                  target_format: str,
                                  timeout: int = 1800) -> Optional[Path]:  # 30 минут для больших файлов
        """
        Конвертация с отслеживанием прогресса и оптимизацией.
        
        Args:
            input_path: Путь к исходному файлу
            target_format: Целевой формат
            timeout: Таймаут в секундах
            
        Returns:
            Путь к конвертированному файлу или None
        """
        start_time = time.time()
        
        try:
            # Проверяем размер файла
            file_size_mb = input_path.stat().st_size / (1024 * 1024)
            
            if self.progress_callback:
                await self.progress_callback(f"📁 Анализ файла ({file_size_mb:.1f} МБ)...")
            
            # Для PDF файлов больше 20 МБ делаем предварительную оптимизацию
            working_file = input_path
            if input_path.suffix.lower() == '.pdf' and file_size_mb > 20:
                working_file = await self.optimize_pdf_before_conversion(input_path)
                file_size_mb = working_file.stat().st_size / (1024 * 1024)
            
            # Генерируем имя выходного файла
            output_filename = self._generate_output_filename(working_file, target_format)
            output_path = working_file.parent / output_filename
            
            # Получаем оптимизированные параметры
            format_params = self.get_optimized_conversion_params(target_format, file_size_mb)
            
            if self.progress_callback:
                estimated_time = self._estimate_conversion_time(file_size_mb, target_format)
                await self.progress_callback(
                    f"⚙️ Начинаю конвертацию в {target_format.upper()}\n"
                    f"⏱️ Ожидаемое время: ~{estimated_time} минут"
                )
            
            # Команда для конвертации
            cmd = [
                'ebook-convert',
                str(working_file),
                str(output_path),
                '--verbose'  # Включаем подробный вывод для отслеживания
            ] + format_params
            
            logger.info(f"Конвертация большого файла: {' '.join(cmd[:3])} + {len(format_params)} параметров")
            
            # Запускаем конвертацию с мониторингом
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            # Мониторим прогресс
            await self._monitor_conversion_progress(process, timeout)
            
            if process.returncode == 0 and output_path.exists():
                duration = time.time() - start_time
                output_size_mb = output_path.stat().st_size / (1024 * 1024)
                
                logger.info(f"Большой файл сконвертирован за {duration/60:.1f} минут")
                
                if self.progress_callback:
                    await self.progress_callback(
                        f"✅ Конвертация завершена!\n"
                        f"⏱️ Время: {duration/60:.1f} минут\n"
                        f"📊 Размер: {output_size_mb:.1f} МБ"
                    )
                
                # Удаляем временный оптимизированный файл
                if working_file != input_path:
                    working_file.unlink()
                
                return output_path
            else:
                logger.error(f"Конвертация большого файла не удалась (код: {process.returncode})")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка конвертации большого файла: {e}")
            return None
    
    async def _monitor_conversion_progress(self, process, timeout):
        """Мониторинг прогресса конвертации."""
        start_time = time.time()
        last_update = start_time
        
        try:
            while True:
                try:
                    # Проверяем, завершился ли процесс
                    line = await asyncio.wait_for(
                        process.stdout.readline(), 
                        timeout=30
                    )
                    
                    if not line:
                        break
                    
                    current_time = time.time()
                    
                    # Отправляем уведомления о прогрессе каждые 2 минуты
                    if self.progress_callback and (current_time - last_update) > 120:
                        elapsed_minutes = (current_time - start_time) / 60
                        await self.progress_callback(
                            f"⏳ Конвертация продолжается...\n"
                            f"⏱️ Прошло: {elapsed_minutes:.1f} минут"
                        )
                        last_update = current_time
                    
                    # Проверяем таймаут
                    if (current_time - start_time) > timeout:
                        process.kill()
                        raise asyncio.TimeoutError("Превышен таймаут конвертации")
                        
                except asyncio.TimeoutError:
                    # Если нет вывода 30 секунд, продолжаем ждать
                    current_time = time.time()
                    if (current_time - start_time) > timeout:
                        process.kill()
                        raise asyncio.TimeoutError("Превышен общий таймаут")
                    continue
            
            # Ждем завершения процесса
            await process.wait()
            
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise
    
    def _estimate_conversion_time(self, file_size_mb: float, target_format: str) -> int:
        """Оценка времени конвертации в минутах."""
        base_time = file_size_mb * 0.1  # 0.1 минуты на МБ базово
        
        # Коэффициенты сложности для разных форматов
        format_multipliers = {
            'txt': 0.5,
            'epub': 1.0,
            'mobi': 1.2,
            'pdf': 1.5,
            'docx': 0.8
        }
        
        multiplier = format_multipliers.get(target_format.lower(), 1.0)
        estimated = int(base_time * multiplier)
        
        return max(1, min(estimated, 30))  # От 1 до 30 минут
    
    def _generate_output_filename(self, input_path: Path, target_format: str) -> str:
        """Генерация имени выходного файла."""
        base_name = input_path.stem
        safe_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).strip()
        
        if len(safe_name) > 50:
            safe_name = safe_name[:50].strip()
        
        if not safe_name:
            safe_name = "Large_Converted_Book"
        
        return f"{safe_name}_Конвертовано.{target_format.lower()}"
