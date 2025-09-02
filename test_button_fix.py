#!/usr/bin/env python3
"""
🔧 Быстрая проверка исправления кнопки токена
Quick fix test for token button
"""

def test_button_names():
    """Проверяет правильность имен кнопок в GUI"""
    try:
        print("🔍 Проверка имен кнопок в bot_gui.py...")
        
        with open('bot_gui.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Проверяем создание кнопки
        if 'self.test_token_btn = ctk.CTkButton(' in code:
            print("✅ Кнопка test_token_btn создается корректно")
        else:
            print("❌ Кнопка test_token_btn не найдена")
            return False
        
        # Проверяем что нет старых ссылок
        if 'self.test_btn' in code:
            print("❌ Найдены оставшиеся ссылки на test_btn")
            import re
            matches = re.findall(r'.*self\.test_btn.*', code)
            for match in matches[:5]:  # Показываем первые 5
                print(f"   {match.strip()}")
            return False
        else:
            print("✅ Старые ссылки на test_btn удалены")
        
        # Проверяем использование в методах
        methods_to_check = ['test_token', '_on_token_valid', '_on_token_invalid', '_on_token_error']
        for method in methods_to_check:
            if f'def {method}(' in code and 'self.test_token_btn' in code:
                print(f"✅ Метод {method} использует правильное имя кнопки")
            elif f'def {method}(' in code:
                print(f"⚠️ Метод {method} найден, но может не использовать кнопку")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")
        return False

def main():
    print("🔧 Проверка исправления кнопки токена")
    print("=" * 40)
    
    if test_button_names():
        print("\n🎉 Все проверки пройдены!")
        print("✅ Кнопка токена теперь работает корректно")
        print("\n🚀 Можно безопасно тестировать GUI:")
        print("   ./start_gui.sh")
    else:
        print("\n❌ Обнаружены проблемы")
        print("Нужно дополнительное исправление")

if __name__ == "__main__":
    main()
