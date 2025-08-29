#!/bin/bash

# Скрипт деплоя на Hetzner
set -e

echo "🚀 Начинаем деплой Telegram Book Converter Bot на Hetzner..."

# Параметры
SERVER_IP="${1:-your_server_ip}"
SERVER_USER="${2:-root}"
BOT_TOKEN="${3}"

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Ошибка: BOT_TOKEN не указан"
    echo "Использование: $0 <server_ip> <server_user> <bot_token>"
    exit 1
fi

# Создаем архив проекта
echo "📦 Создаем архив проекта..."
tar -czf telegram-bot.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='logs' \
    --exclude='temp' \
    --exclude='*.log' \
    .

# Копируем на сервер
echo "📤 Загружаем файлы на сервер..."
scp telegram-bot.tar.gz $SERVER_USER@$SERVER_IP:/tmp/

# Подключаемся к серверу и деплоим
echo "🔧 Настраиваем на сервере..."
ssh $SERVER_USER@$SERVER_IP << EOF
set -e

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
mkdir -p /opt/telegram-bot
cd /opt/telegram-bot

# Останавливаем старую версию если запущена
if [ -f docker-compose.yml ]; then
    echo "⏹️ Останавливаем старую версию..."
    docker-compose down || true
fi

# Извлекаем новые файлы
echo "📂 Извлекаем файлы..."
tar -xzf /tmp/telegram-bot.tar.gz
rm /tmp/telegram-bot.tar.gz

# Создаем .env файл
echo "⚙️ Настраиваем окружение..."
cat > .env << EOL
BOT_TOKEN=$BOT_TOKEN
PRODUCTION=1
LOG_LEVEL=INFO
CONVERSION_TIMEOUT=300
EOL

# Создаем директории
mkdir -p logs temp

# Собираем и запускаем Docker контейнер
echo "🔨 Собираем Docker образ..."
docker-compose build

echo "🚀 Запускаем бота..."
docker-compose up -d

echo "✅ Деплой завершен!"
echo "📊 Проверьте статус: docker-compose logs -f"
EOF

# Очищаем локальный архив
rm telegram-bot.tar.gz

echo ""
echo "🎉 Деплой завершен успешно!"
echo "📍 Сервер: $SERVER_IP"
echo "🤖 Бот должен быть запущен и работать"
echo ""
echo "Полезные команды для управления:"
echo "  ssh $SERVER_USER@$SERVER_IP 'cd /opt/telegram-bot && docker-compose logs -f'"
echo "  ssh $SERVER_USER@$SERVER_IP 'cd /opt/telegram-bot && docker-compose restart'"
echo "  ssh $SERVER_USER@$SERVER_IP 'cd /opt/telegram-bot && docker-compose down'"
echo ""
