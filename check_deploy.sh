#!/bin/bash

# Скрипт проверки готовности к деплою
set -e

echo "🔍 Проверка готовности к деплою..."

# Проверяем наличие необходимых файлов
REQUIRED_FILES=(
    "bot.py"
    "requirements.txt"
    "Dockerfile"
    "docker-compose.yml"
    ".dockerignore"
    "deploy.sh"
    "DEPLOY.md"
)

echo "📋 Проверяем файлы..."
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file отсутствует"
        exit 1
    fi
done

# Проверяем синтаксис Python файлов
echo ""
echo "🐍 Проверяем синтаксис Python..."
find . -name "*.py" -not -path "./venv/*" | while read file; do
    if python -m py_compile "$file" 2>/dev/null; then
        echo "✅ $file"
    else
        echo "❌ Ошибка синтаксиса в $file"
        exit 1
    fi
done

# Проверяем зависимости
echo ""
echo "📦 Проверяем зависимости..."
if [ -f "requirements.txt" ]; then
    # Создаем временное виртуальное окружение для проверки
    python3 -m venv test_env
    source test_env/bin/activate
    
    if pip install -r requirements.txt > /dev/null 2>&1; then
        echo "✅ Все зависимости устанавливаются"
    else
        echo "❌ Проблема с зависимостями"
        deactivate
        rm -rf test_env
        exit 1
    fi
    
    deactivate
    rm -rf test_env
fi

# Проверяем Docker файлы
echo ""
echo "🐳 Проверяем Docker конфигурацию..."
if command -v docker &> /dev/null; then
    if docker build -t telegram-bot-test . > /dev/null 2>&1; then
        echo "✅ Docker образ собирается успешно"
        docker rmi telegram-bot-test > /dev/null 2>&1
    else
        echo "❌ Ошибка сборки Docker образа"
        exit 1
    fi
else
    echo "⚠️ Docker не установлен, пропускаем проверку образа"
fi

# Проверяем размер проекта
echo ""
echo "📏 Анализ размера проекта..."
SIZE=$(du -sh . --exclude=venv --exclude=test_env 2>/dev/null | cut -f1)
echo "📊 Размер проекта (без venv): $SIZE"

# Создаем архив для деплоя
echo ""
echo "📦 Создаем тестовый архив..."
tar -czf test-deploy.tar.gz \
    --exclude='venv' \
    --exclude='test_env' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='logs' \
    --exclude='temp' \
    --exclude='*.log' \
    .

ARCHIVE_SIZE=$(du -sh test-deploy.tar.gz | cut -f1)
echo "📊 Размер архива: $ARCHIVE_SIZE"
rm test-deploy.tar.gz

echo ""
echo "🎉 Проверка завершена успешно!"
echo ""
echo "📋 Готово к деплою:"
echo "  🐳 Docker образ собирается"
echo "  📦 Зависимости корректны"
echo "  🐍 Синтаксис Python корректен"
echo "  📁 Все необходимые файлы присутствуют"
echo ""
echo "🚀 Для деплоя используйте:"
echo "  ./deploy.sh <server_ip> <username> <bot_token>"
echo ""
