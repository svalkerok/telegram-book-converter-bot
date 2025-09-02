@echo off
chcp 65001 >nul
echo 🤖 Telegram Book Converter Bot - GUI Manager
echo ===============================================
echo.

REM Проверяем наличие основного файла
if not exist "TelegramBotGUI.exe" (
    echo ❌ Файл TelegramBotGUI.exe не найден!
    echo 📁 Убедитесь что вы запускаете из правильной папки
    echo.
    pause
    exit /b 1
)

echo 🚀 Запуск GUI приложения...
echo 💡 Если появится предупреждение Windows - разрешите запуск
echo.

REM Запускаем приложение
start "" "TelegramBotGUI.exe"

REM Ждем 3 секунды и закрываем консоль
timeout /t 3 /nobreak >nul
exit
