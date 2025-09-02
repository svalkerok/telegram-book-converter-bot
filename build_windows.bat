@echo off
setlocal enabledelayedexpansion

:: 🏗️ Скрипт сборки Windows EXE файла
:: Build script for Windows EXE file

echo [BUILD] Начинаем сборку Windows EXE файла...

:: Проверка виртуального окружения
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Активация виртуального окружения...
    call venv\Scripts\activate.bat
    echo [INFO] ✅ Виртуальное окружение активировано
) else (
    echo [ERROR] Виртуальное окружение не найдено!
    echo [INFO] Создайте виртуальное окружение: python -m venv venv
    pause
    exit /b 1
)

:: Проверка зависимостей
echo [BUILD] 🔍 Проверка зависимостей...

:: Проверяем PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [INFO] 📦 Установка PyInstaller...
    pip install pyinstaller
)

:: Проверяем Pillow
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo [INFO] 📦 Установка Pillow...
    pip install Pillow
)

:: Проверяем основные зависимости
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo [ERROR] ❌ customtkinter не найден!
    echo [INFO] Установите: pip install customtkinter
    pause
    exit /b 1
)

python -c "import requests" 2>nul
if errorlevel 1 (
    echo [ERROR] ❌ requests не найден!
    echo [INFO] Установите: pip install requests
    pause
    exit /b 1
)

python -c "import dotenv" 2>nul
if errorlevel 1 (
    echo [ERROR] ❌ python-dotenv не найден!
    echo [INFO] Установите: pip install python-dotenv
    pause
    exit /b 1
)

echo [INFO] ✅ Все зависимости проверены

:: Создание иконки
echo [BUILD] 🎨 Создание иконки...
if not exist "bot_icon.ico" (
    python create_icon.py
) else (
    echo [INFO] ✅ Иконка уже существует
)

:: Очистка предыдущих сборок
echo [BUILD] 🧹 Очистка предыдущих сборок...
if exist "build" (
    rmdir /s /q build
    echo [INFO] ✅ Директория build очищена
)

if exist "dist" (
    rmdir /s /q dist
    echo [INFO] ✅ Директория dist очищена
)

if exist "TelegramBotGUI.exe" (
    del "TelegramBotGUI.exe"
    echo [INFO] ✅ Старый EXE файл удален
)

:: Сборка с PyInstaller
echo [BUILD] 🚀 Сборка исполняемого файла...
pyinstaller bot_gui.spec --clean --noconfirm

if errorlevel 1 (
    echo [ERROR] ❌ Ошибка при сборке!
    pause
    exit /b 1
)

:: Перемещение результата
if exist "dist\TelegramBotGUI.exe" (
    move "dist\TelegramBotGUI.exe" "TelegramBotGUI.exe"
    echo [INFO] ✅ EXE файл перемещен в корневую директорию
) else (
    echo [ERROR] ❌ EXE файл не найден в dist/
    pause
    exit /b 1
)

:: Создание дистрибутива
echo [BUILD] 📦 Создание дистрибутива...
if exist "TelegramBotGUI_Distribution" (
    rmdir /s /q "TelegramBotGUI_Distribution"
)

mkdir "TelegramBotGUI_Distribution"
copy "TelegramBotGUI.exe" "TelegramBotGUI_Distribution\"
copy "README.md" "TelegramBotGUI_Distribution\"
copy "GUI_GUIDE.md" "TelegramBotGUI_Distribution\"
copy "WINDOWS_SETUP.md" "TelegramBotGUI_Distribution\"

:: Создание start.bat
echo @echo off > "TelegramBotGUI_Distribution\start.bat"
echo echo Запуск Telegram Bot GUI... >> "TelegramBotGUI_Distribution\start.bat"
echo TelegramBotGUI.exe >> "TelegramBotGUI_Distribution\start.bat"
echo pause >> "TelegramBotGUI_Distribution\start.bat"

echo [INFO] ✅ Дистрибутив создан в TelegramBotGUI_Distribution/

:: Создание архива
echo [BUILD] 📁 Создание архива...
if exist "TelegramBotGUI_Windows.zip" (
    del "TelegramBotGUI_Windows.zip"
)

:: Используем PowerShell для создания zip архива
powershell -command "Compress-Archive -Path 'TelegramBotGUI_Distribution\*' -DestinationPath 'TelegramBotGUI_Windows.zip'"

if exist "TelegramBotGUI_Windows.zip" (
    echo [INFO] ✅ Архив TelegramBotGUI_Windows.zip создан
) else (
    echo [WARNING] ⚠️ Не удалось создать архив
)

:: Очистка временных файлов
echo [BUILD] 🧹 Очистка временных файлов...
if exist "build" (
    rmdir /s /q build
)
if exist "dist" (
    rmdir /s /q dist
)

:: Результат
echo.
echo [BUILD] 🎉 Сборка завершена успешно!
echo.
echo 📁 Результаты:
echo    - TelegramBotGUI.exe (исполняемый файл)
echo    - TelegramBotGUI_Distribution/ (дистрибутив)
echo    - TelegramBotGUI_Windows.zip (архив для распространения)
echo.
echo 🚀 Для запуска: TelegramBotGUI.exe
echo 📖 Инструкции: README.md в дистрибутиве
echo.

pause
