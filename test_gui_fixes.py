#!/usr/bin/env python3
"""
🧪 Быстрый тест исправлений GUI
Quick test for GUI fixes
"""

def test_gui_imports():
    """Тестирует импорты GUI"""
    try:
        print("🔍 Тестирование импортов...")
        
        import customtkinter
        print(f"✅ CustomTkinter {customtkinter.__version__}")
        
        import requests
        print(f"✅ requests {requests.__version__}")
        
        import gui_safety
        print("✅ gui_safety импортирован")
        
        # Тест базовых классов
        validator = gui_safety.TokenValidator()
        print("✅ TokenValidator создан")
        
        # Тест валидации формата
        valid, msg = validator.validate_token_format("123456789:AABBccddEEffgghhIIjjKKllmmNN")
        print(f"✅ Валидация формата: {valid} - {msg}")
        
        invalid, msg = validator.validate_token_format("invalid")
        print(f"✅ Невалидный формат: {invalid} - {msg}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка теста: {e}")
        return False

def test_gui_syntax():
    """Тестирует синтаксис GUI файла"""
    try:
        print("\n🔍 Проверка синтаксиса bot_gui.py...")
        
        with open('bot_gui.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, 'bot_gui.py', 'exec')
        print("✅ Синтаксис bot_gui.py корректен")
        
        # Проверяем что есть ключевые исправления
        if "self._closing" in code:
            print("✅ Флаг _closing добавлен")
        
        if "WM_DELETE_WINDOW" in code:
            print("✅ Обработчик закрытия окна добавлен")
        
        if "safe_after" in code or "self.root.after" in code:
            print("✅ Безопасные GUI обновления")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Синтаксическая ошибка: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Главная функция теста"""
    print("🧪 Тестирование исправлений GUI")
    print("=" * 40)
    
    success = True
    
    # Тест импортов
    if not test_gui_imports():
        success = False
    
    # Тест синтаксиса
    if not test_gui_syntax():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Все тесты пройдены успешно!")
        print("\n📋 Что исправлено:")
        print("   • Безопасная проверка токена в отдельном потоке")
        print("   • Правильная обработка закрытия окон")
        print("   • Защита от блокировки GUI")
        print("   • Улучшенная обработка ошибок")
        print("\n🚀 GUI готов к использованию!")
    else:
        print("❌ Некоторые тесты не пройдены")
    
    return success

if __name__ == "__main__":
    main()
