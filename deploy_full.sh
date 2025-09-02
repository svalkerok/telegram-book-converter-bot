#!/bin/bash

# Полный деплой Telegram Book Converter Bot на Hetzner с исправлениями
set -e

echo "🚀 Полный деплой Telegram Book Converter Bot на Hetzner..."

# Параметры
SERVER_IP="37.27.193.227"
SERVER_USER="root"
BOT_TOKEN="8065886351:AAFvMyd8WZX1YC-ccnGlr70_tBY7xZYCprQ"

echo "📦 Создаем архив проекта..."
tar -czf telegram-bot-full.tar.gz \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='logs' \
    --exclude='temp' \
    --exclude='*.log' \
    --exclude='TelegramBotGUI*' \
    --exclude='build_*' \
    --exclude='gui_*' \
    --exclude='bot_gui*' \
    --exclude='*.exe' \
    --exclude='*.zip' \
    .

echo "📤 Загружаем файлы на сервер..."
scp telegram-bot-full.tar.gz $SERVER_USER@$SERVER_IP:/tmp/

echo "🔧 Настраиваем на сервере..."
ssh $SERVER_USER@$SERVER_IP << EOF
set -e

# Обновляем систему
echo "🔄 Обновляем систему..."
apt update

# Устанавливаем необходимые пакеты
echo "📚 Устанавливаем необходимые пакеты..."
apt install -y calibre curl wget

# Устанавливаем Docker если не установлен
if ! command -v docker &> /dev/null; then
    echo "🐳 Устанавливаем Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
fi

# Устанавливаем Docker Compose если не установлен
if ! command -v docker-compose &> /dev/null; then
    echo "🐙 Устанавливаем Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Создаем директорию для приложения
echo "📁 Создаем директорию приложения..."
mkdir -p /opt/telegram-book-converter
cd /opt/telegram-book-converter

# Извлекаем файлы
echo "📂 Извлекаем файлы..."
tar -xzf /tmp/telegram-bot-full.tar.gz
rm /tmp/telegram-bot-full.tar.gz

# Создаем .env файл с нашими настройками
echo "⚙️ Настраиваем окружение..."
cat > .env << EOL
BOT_TOKEN=$BOT_TOKEN
PRODUCTION=1
TEMP_DIR=/app/temp
LOG_LEVEL=INFO
CONVERSION_TIMEOUT=300
MAX_FILE_SIZE=52428800
EOL

# Создаем необходимые директории
mkdir -p logs temp

# Проверяем, что Calibre установлен
echo "🔍 Проверяем Calibre..."
ebook-convert --version

# Собираем Docker образ
echo "🔨 Собираем Docker образ..."
docker-compose build

# Запускаем бота
echo "🚀 Запускаем бота..."
docker-compose up -d

# Ждем запуска
sleep 10

# Проверяем статус
echo "📊 Проверяем статус..."
docker-compose ps
docker-compose logs --tail=20

echo ""
echo "✅ Деплой завершен успешно!"
echo "🤖 Бот запущен с токеном: $BOT_TOKEN"
echo "📍 Сервер: $SERVER_IP"
echo ""
EOF

# Очищаем локальный архив
rm telegram-bot-full.tar.gz

echo ""
echo "🎉 Полный деплой завершен успешно!"
echo "🔧 Применены все исправления:"
echo "   ✅ Исправление ошибки E999 для Kindle"
echo "   ✅ Улучшенные названия файлов"
echo "   ✅ Оптимизированные параметры EPUB"
echo "   ✅ Улучшенные сообщения пользователю"
echo ""
echo "📱 Тестирование:"
echo "   1. Найдите бота в Telegram"
echo "   2. Отправьте /start"
echo "   3. Загрузите HTML файл"
echo "   4. Конвертируйте в EPUB"
echo "   5. Проверьте название и совместимость с Kindle"
echo ""
echo "Команды для мониторинга:"
echo "  ssh $SERVER_USER@$SERVER_IP 'cd /opt/telegram-book-converter && docker-compose logs -f'"
echo "  ssh $SERVER_USER@$SERVER_IP 'cd /opt/telegram-book-converter && docker-compose ps'"
echo ""
