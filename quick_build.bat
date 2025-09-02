@echo off
title Telegram Bot - Быстрая сборка Windows EXE

echo ===============================================
echo      Быстрая сборка Telegram Bot GUI
echo ===============================================
echo.

:: Проверка виртуального окружения
if not exist "venv\Scripts\activate.bat" (
    echo [1/6] Создание виртуального окружения...
    python -m venv venv
    if errorlevel 1 (
        echo ОШИБКА: Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
) else (
    echo [1/6] Виртуальное окружение найдено ✓
)

:: Активация окружения
echo [2/6] Активация окружения...
call venv\Scripts\activate.bat

:: Установка зависимостей
echo [3/6] Установка зависимостей...
pip install --quiet aiogram python-dotenv aiofiles customtkinter requests pyinstaller pillow

:: Создание иконки
echo [4/6] Создание иконки...
if not exist "bot_icon.ico" (
    python create_icon.py > nul 2>&1
)

:: Сборка
echo [5/6] Сборка exe файла...
pyinstaller bot_gui.spec --clean --noconfirm --log-level ERROR

:: Перемещение и очистка
echo [6/6] Финализация...
if exist "dist\TelegramBotGUI.exe" (
    move "dist\TelegramBotGUI.exe" "TelegramBotGUI_NEW.exe" > nul
    rmdir /s /q build dist 2>nul
    
    echo.
    echo =============================================== 
    echo            СБОРКА ЗАВЕРШЕНА УСПЕШНО!
    echo ===============================================
    echo.
    echo Результат: TelegramBotGUI_NEW.exe
    echo Размер: 
    for %%I in (TelegramBotGUI_NEW.exe) do echo    %%~zI байт (~%%~zI/1000000 MB)
    echo.
    echo Для запуска: TelegramBotGUI_NEW.exe
    echo.
) else (
    echo.
    echo ===============================================
    echo              ОШИБКА СБОРКИ!
    echo ===============================================
    echo.
    echo Проверьте логи выше для диагностики
    echo.
)

pause
