#!/usr/bin/env python3
"""
🚀 Telegram Book Converter Bot - Windows Launcher
Главный файл для запуска GUI приложения в Windows
"""

import sys
import os
import traceback
from pathlib import Path

def setup_environment():
    """Настраиваем окружение для приложения"""
    # Добавляем текущую директорию в путь
    current_dir = Path(__file__).parent.absolute()
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Устанавливаем рабочую директорию
    os.chdir(current_dir)
    
    return current_dir

def check_dependencies():
    """Проверяем наличие всех необходимых зависимостей"""
    missing_deps = []
    
    try:
        import customtkinter
    except ImportError:
        missing_deps.append('customtkinter')
    
    try:
        import requests
    except ImportError:
        missing_deps.append('requests')
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append('tkinter')
    
    return missing_deps

def show_error_dialog(title, message):
    """Показывает диалог с ошибкой"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Скрываем главное окно
        messagebox.showerror(title, message)
        root.destroy()
    except:
        # Если tkinter недоступен, выводим в консоль
        print(f"ERROR: {title}")
        print(message)

def main():
    """Главная функция запуска приложения"""
    try:
        # Настраиваем окружение
        app_dir = setup_environment()
        print(f"🚀 Запуск Telegram Bot GUI Manager...")
        print(f"📁 Рабочая директория: {app_dir}")
        
        # Проверяем зависимости
        missing_deps = check_dependencies()
        if missing_deps:
            error_msg = f"Отсутствуют зависимости:\n{', '.join(missing_deps)}\n\nУстановите их командой:\npip install {' '.join(missing_deps)}"
            show_error_dialog("Ошибка зависимостей", error_msg)
            return 1
        
        # Импортируем и запускаем GUI
        print("📦 Загрузка модулей...")
        
        # Импортируем основные модули
        import bot_gui
        
        print("🎨 Запуск графического интерфейса...")
        
        # Создаем и запускаем приложение
        app = bot_gui.BotManagerGUI()
        
        print("✅ GUI загружен успешно!")
        print("🎯 Управление ботом готово к использованию")
        
        # Запускаем главный цикл
        app.run()
        
        return 0
        
    except ImportError as e:
        error_msg = f"Ошибка импорта модуля:\n{e}\n\nПроверьте установку зависимостей."
        print(f"❌ {error_msg}")
        show_error_dialog("Ошибка импорта", error_msg)
        return 1
        
    except Exception as e:
        error_msg = f"Неожиданная ошибка:\n{e}\n\nПодробности:\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")
        show_error_dialog("Критическая ошибка", error_msg)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
