#!/bin/bash

# Скрипт для запуска Telegram Book Converter Bot

echo "🚀 Запуск Telegram Book Converter Bot..."
echo ""

# Переходим в директорию проекта
cd "$(dirname "$0")"

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "Создаю виртуальное окружение..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Проверяем наличие зависимостей
if [ ! -f "venv/pyvenv.cfg" ] || ! python -c "import aiogram" 2>/dev/null; then
    echo "📦 Устанавливаю зависимости..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Зависимости установлены"
fi

# Проверяем наличие токена
if ! grep -q "BOT_TOKEN=" .env || grep -q "your_bot_token_here" .env; then
    echo ""
    echo "⚠️  ВНИМАНИЕ: Не найден токен бота!"
    echo ""
    echo "Чтобы запустить бота:"
    echo "1. Получите токен у @BotFather в Telegram"
    echo "2. Откройте файл .env"
    echo "3. Замените 'your_bot_token_here' на ваш токен"
    echo ""
    echo "Подробные инструкции в файле SETUP.md"
    exit 1
fi

# Проверяем Calibre
if ! command -v ebook-convert &> /dev/null; then
    echo ""
    echo "⚠️  ВНИМАНИЕ: Calibre не установлен!"
    echo ""
    echo "Установите Calibre:"
    echo "sudo apt install calibre"
    echo ""
    exit 1
fi

# Запускаем бота
echo ""
echo "✅ Все проверки пройдены"
echo "🤖 Запускаю бота..."
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

python bot.py
