#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Book Converter Bot - Simple Windows Launcher
Упрощенный запуск GUI приложения без настройки кодировки
"""

import sys
import os
import traceback
from pathlib import Path

def safe_print(message):
    """Безопасный вывод сообщений"""
    # Заменяем проблемные символы
    try:
        print(message.encode('ascii', errors='replace').decode('ascii'))
    except:
        print("[MESSAGE] Сообщение содержит недоступные символы")

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
        safe_print(f"ERROR: {title}")
        safe_print(message)

def main():
    """Главная функция запуска приложения"""
    try:
        # Настраиваем окружение
        app_dir = setup_environment()
        safe_print("[LAUNCH] Запуск Telegram Bot GUI Manager...")
        safe_print(f"[INFO] Рабочая директория: {app_dir}")
        
        # Проверяем зависимости
        missing_deps = check_dependencies()
        if missing_deps:
            error_msg = f"Отсутствуют зависимости:\n{', '.join(missing_deps)}\n\nУстановите их командой:\npip install {' '.join(missing_deps)}"
            show_error_dialog("Ошибка зависимостей", error_msg)
            return 1
        
        # Импортируем и запускаем GUI
        safe_print("[LOAD] Загрузка модулей...")
        
        # Импортируем основные модули
        import bot_gui
        
        safe_print("[GUI] Запуск графического интерфейса...")
        
        # Создаем и запускаем приложение
        app = bot_gui.BotManagerGUI()
        
        safe_print("[OK] GUI загружен успешно!")
        safe_print("[READY] Управление ботом готово к использованию")
        
        # Запускаем главный цикл
        app.run()
        
        return 0
        
    except ImportError as e:
        error_msg = f"Ошибка импорта модуля:\n{e}\n\nПроверьте установку зависимостей."
        safe_print(f"[ERROR] {error_msg}")
        show_error_dialog("Ошибка импорта", error_msg)
        return 1
        
    except Exception as e:
        error_msg = f"Неожиданная ошибка:\n{e}\n\nПодробности:\n{traceback.format_exc()}"
        safe_print(f"[ERROR] {error_msg}")
        show_error_dialog("Критическая ошибка", error_msg)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
