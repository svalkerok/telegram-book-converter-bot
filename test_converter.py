#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы конвертера без Telegram бота.
"""
import asyncio
import tempfile
from pathlib import Path
from converter.converter import BookConverter

async def test_converter():
    """Тест конвертера с демо-файлом."""
    
    # Создаем простой HTML файл для тестирования
    test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Тестовая книга</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Глава 1: Введение</h1>
    <p>Это тестовая книга для проверки работы конвертера.</p>
    <p>Конвертер способен преобразовывать книги между различными форматами.</p>
    
    <h2>Возможности</h2>
    <ul>
        <li>Конвертация PDF в EPUB</li>
        <li>Конвертация EPUB в MOBI</li>
        <li>Конвертация FB2 в PDF</li>
        <li>И многое другое!</li>
    </ul>
    
    <h1>Глава 2: Заключение</h1>
    <p>Тестирование прошло успешно!</p>
</body>
</html>
    """
    
    converter = BookConverter()
    
    # Создаем временный HTML файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(test_html)
        input_path = Path(f.name)
    
    try:
        print(f"🔄 Тестирую конвертацию HTML -> EPUB...")
        print(f"📂 Входной файл: {input_path}")
        
        # Конвертируем в EPUB
        output_path = await converter.convert(input_path, 'epub')
        
        if output_path and output_path.exists():
            print(f"✅ Конвертация прошла успешно!")
            print(f"📄 Выходной файл: {output_path}")
            print(f"📊 Размер: {output_path.stat().st_size // 1024} КБ")
            
            # Удаляем выходной файл
            output_path.unlink()
            print("🗑️ Выходной файл удален")
        else:
            print("❌ Ошибка конвертации")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        
    finally:
        # Удаляем входной файл
        if input_path.exists():
            input_path.unlink()
            print("🗑️ Входной файл удален")

if __name__ == "__main__":
    print("🧪 Тестирование конвертера книг...")
    asyncio.run(test_converter())
    print("✨ Тестирование завершено!")
