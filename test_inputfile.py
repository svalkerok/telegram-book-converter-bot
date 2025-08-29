#!/usr/bin/env python3
"""
Тест FSInputFile для проверки корректности исправления.
"""
from aiogram.types import FSInputFile
from pathlib import Path
import tempfile

def test_fsinputfile():
    """Тестируем создание FSInputFile"""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('Test content')
        temp_path = Path(f.name)
    
    try:
        # Создаем FSInputFile
        input_file = FSInputFile(temp_path, filename='test.txt')
        print(f"✅ FSInputFile создан успешно: {input_file}")
        print(f"✅ Имя файла: {input_file.filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания FSInputFile: {e}")
        return False
    finally:
        # Удаляем временный файл
        temp_path.unlink(missing_ok=True)

if __name__ == "__main__":
    success = test_fsinputfile()
    print(f"Тест {'✅ ПРОШЕЛ' if success else '❌ НЕ ПРОШЕЛ'}")
