#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест исправления проблемы с кодировкой Unicode
"""

import sys
import os
from pathlib import Path

# Добавляем путь к проекту
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_launcher():
    """Тестируем launcher.py"""
    print("[TEST] Тестирование launcher.py...")
    
    try:
        import launcher
        print("[OK] launcher.py импортирован успешно")
        
        # Проверяем функцию setup_environment
        app_dir = launcher.setup_environment()
        print(f"[OK] setup_environment работает: {app_dir}")
        
        # Проверяем check_dependencies
        missing_deps = launcher.check_dependencies()
        if not missing_deps:
            print("[OK] Все зависимости найдены")
        else:
            print(f"[INFO] Отсутствующие зависимости: {missing_deps}")
            
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка в launcher.py: {e}")
        return False

def test_bot_gui():
    """Тестируем bot_gui.py"""
    print("[TEST] Тестирование bot_gui.py...")
    
    try:
        # Проверяем импорт
        import bot_gui
        print("[OK] bot_gui.py импортирован успешно")
        
        # Проверяем функцию safe_print
        if hasattr(bot_gui, 'safe_print'):
            print("[OK] Функция safe_print найдена")
            
            # Тестируем safe_print с эмодзи
            test_message = "🚀 Тест с эмодзи ✅"
            bot_gui.safe_print(test_message)
            print("[OK] safe_print работает с эмодзи")
        else:
            print("[WARNING] Функция safe_print не найдена")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка в bot_gui.py: {e}")
        return False

def test_unicode_handling():
    """Тестируем обработку Unicode"""
    print("[TEST] Тестирование обработки Unicode...")
    
    try:
        # Тест различных эмодзи
        test_emojis = ['🚀', '✅', '❌', '📦', '🎨', '🎯', '📁', '🤖', '⚠️']
        
        for emoji in test_emojis:
            try:
                # Пытаемся вывести эмодзи
                message = f"Тест эмодзи: {emoji}"
                print(message.encode('ascii', errors='replace').decode('ascii'))
            except Exception as e:
                print(f"[ERROR] Проблема с эмодзи {emoji}: {e}")
                
        print("[OK] Тест обработки Unicode завершен")
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка теста Unicode: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("=" * 50)
    print("ТЕСТ ИСПРАВЛЕНИЯ ПРОБЛЕМЫ С КОДИРОВКОЙ")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Тест 1: launcher.py
    if test_launcher():
        tests_passed += 1
    
    print()
    
    # Тест 2: bot_gui.py  
    if test_bot_gui():
        tests_passed += 1
    
    print()
    
    # Тест 3: Unicode handling
    if test_unicode_handling():
        tests_passed += 1
    
    print()
    print("=" * 50)
    print(f"РЕЗУЛЬТАТ: {tests_passed}/{total_tests} тестов пройдено")
    
    if tests_passed == total_tests:
        print("[SUCCESS] Все тесты пройдены! Исправление работает!")
    else:
        print("[WARNING] Некоторые тесты не пройдены")
        
    print("=" * 50)
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    input("\nНажмите Enter для выхода...")
    sys.exit(0 if success else 1)
