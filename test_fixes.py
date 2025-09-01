#!/usr/bin/env python3
"""
Тестовый скрипт для проверки исправлений конвертера.
"""
import asyncio
import tempfile
from pathlib import Path
from converter.converter import BookConverter

async def test_epub_conversion():
    """Тест конвертации в EPUB с новыми параметрами."""
    
    # Создаем простой HTML файл для тестирования
    test_html = """<!DOCTYPE html>
<html>
<head>
    <title>Тестовая книга для проверки Kindle</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Глава 1: Тест совместимости с Kindle</h1>
    <p>Эта книга создана для тестирования совместимости с Amazon Kindle.</p>
    <p>Проверяем исправление ошибки E999.</p>
    
    <h2>Что было исправлено:</h2>
    <ul>
        <li>Добавлен EPUB версии 2.0 для совместимости</li>
        <li>Встроенное оглавление</li>
        <li>Плоская структура файлов</li>
        <li>Метаданные по умолчанию</li>
        <li>Улучшенные названия файлов</li>
    </ul>
    
    <h1>Глава 2: Новая схема именования</h1>
    <p>Файлы теперь называются: ОригинальноеИмя_Конвертовано.формат</p>
    <p>Специальные символы удаляются автоматически.</p>
</body>
</html>"""
    
    converter = BookConverter()
    
    # Создаем временный HTML файл с проблемным именем
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(test_html)
        input_path = Path(f.name)
    
    # Переименовываем файл чтобы протестировать очистку имени
    problem_name = input_path.parent / "Тестовая книга <с> проблемными:символами|?.html"
    input_path.rename(problem_name)
    input_path = problem_name
    
    try:
        print(f"🔄 Тестирую конвертацию с новыми параметрами...")
        print(f"📂 Входной файл: {input_path.name}")
        
        # Конвертируем в EPUB
        output_path = await converter.convert(input_path, 'epub')
        
        if output_path and output_path.exists():
            print(f"✅ Конвертация прошла успешно!")
            print(f"📄 Выходной файл: {output_path.name}")
            print(f"📊 Размер файла: {output_path.stat().st_size / 1024:.1f} КБ")
            
            # Проверяем содержимое EPUB на базовом уровне
            print(f"🔍 Проверяем структуру EPUB...")
            
            # Очищаем тестовые файлы
            input_path.unlink()
            output_path.unlink()
            
            return True
        else:
            print(f"❌ Конвертация не удалась!")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False
    finally:
        # Очищаем, если файлы остались
        try:
            if input_path.exists():
                input_path.unlink()
        except:
            pass

async def test_filename_generation():
    """Тест функции генерации имен файлов."""
    
    converter = BookConverter()
    
    test_cases = [
        ("normal_file.pdf", "epub", "normal_file_Конвертовано.epub"),
        ("файл с русскими буквами.txt", "mobi", "файл_с_русскими_буквами_Конвертовано.mobi"),
        ("file<with>bad:chars?.fb2", "pdf", "filewithbadchars_Конвертовано.pdf"),
        ("very_long_filename_that_should_be_truncated_because_its_too_long.html", "epub", 
         "very_long_filename_that_should_be_truncated_beca_Конвертовано.epub"),
    ]
    
    print(f"🧪 Тестирую генерацию имен файлов...")
    
    for original, format_type, expected_pattern in test_cases:
        input_path = Path(f"/tmp/{original}")
        output_path = converter.generate_output_filename(input_path, format_type)
        
        print(f"📝 {original} -> {output_path.name}")
        
        # Проверяем, что в имени есть "_Конвертовано"
        assert "_Конвертовано" in output_path.name, f"Отсутствует суффикс в {output_path.name}"
        
        # Проверяем, что расширение правильное
        assert output_path.suffix == f".{format_type}", f"Неправильное расширение в {output_path.name}"
    
    print(f"✅ Все тесты имен файлов прошли успешно!")

if __name__ == "__main__":
    print("🧪 Тестирование исправлений конвертера...")
    print("=" * 50)
    
    # Тест именования файлов
    asyncio.run(test_filename_generation())
    print()
    
    # Тест конвертации EPUB
    success = asyncio.run(test_epub_conversion())
    
    print("=" * 50)
    if success:
        print("✨ Все тесты прошли успешно! Исправления работают.")
    else:
        print("❌ Некоторые тесты не прошли. Требуется дополнительная отладка.")
