#!/bin/bash

# Скрипт быстрого обновления исправлений на Hetzner
set -e

echo "🔄 Обновляем исправления Telegram Book Converter Bot на Hetzner..."

# Параметры
SERVER_IP="${1:-37.27.193.227}"
SERVER_USER="${2:-root}"

if [ $# -lt 2 ]; then
    echo "Использование: $0 <server_ip> <server_user>"
    echo "Пример: $0 37.27.193.227 root"
    exit 1
fi

echo "📋 Подготавливаем файлы для обновления..."

# Создаем временную директорию для измененных файлов
mkdir -p update_files/converter
mkdir -p update_files/handlers
mkdir -p update_files/docs

# Копируем только измененные файлы
echo "📦 Собираем измененные файлы..."
cp converter/converter.py update_files/converter/
cp handlers/callbacks.py update_files/handlers/
cp test_fixes.py update_files/
cp KINDLE_FIX.md update_files/docs/
cp test_kindle_book.html update_files/

# Создаем архив только с обновлениями
tar -czf kindle_fixes.tar.gz -C update_files .

echo "📤 Загружаем обновления на сервер..."
scp kindle_fixes.tar.gz $SERVER_USER@$SERVER_IP:/tmp/

# Применяем обновления на сервере
echo "🔧 Применяем исправления на сервере..."
ssh $SERVER_USER@$SERVER_IP << EOF
set -e

cd /opt/telegram-book-converter

# Создаем резервную копию
echo "💾 Создаем резервную копию..."
cp -r converter converter_backup_\$(date +%Y%m%d_%H%M%S) || true
cp -r handlers handlers_backup_\$(date +%Y%m%d_%H%M%S) || true

# Применяем обновления
echo "📂 Применяем новые файлы..."
tar -xzf /tmp/kindle_fixes.tar.gz
rm /tmp/kindle_fixes.tar.gz

# Перезапускаем бота
echo "🔄 Перезапускаем бота..."
docker-compose restart

# Ждем немного для запуска
sleep 5

# Проверяем статус
echo "📊 Проверяем статус..."
docker-compose ps

echo ""
echo "✅ Обновление завершено!"
echo "🔍 Проверьте логи: docker-compose logs -f telegram-bot"
EOF

# Очищаем временные файлы
rm -rf update_files
rm kindle_fixes.tar.gz

echo ""
echo "🎉 Обновление исправлений завершено успешно!"
echo "📍 Сервер: $SERVER_IP"
echo "🔧 Применены исправления:"
echo "   ✅ Исправление ошибки E999 для Kindle"
echo "   ✅ Улучшенные названия файлов"
echo "   ✅ Оптимизированные параметры EPUB"
echo "   ✅ Улучшенные сообщения пользователю"
echo ""
echo "📱 Тестирование:"
echo "   1. Отправьте HTML файл боту"
echo "   2. Конвертируйте в EPUB"
echo "   3. Проверьте название файла и совместимость с Kindle"
echo ""
echo "Команды для мониторинга:"
echo "  ssh $SERVER_USER@$SERVER_IP 'cd /opt/telegram-book-converter && docker-compose logs -f'"
echo "  ssh $SERVER_USER@$SERVER_IP 'cd /opt/telegram-book-converter && docker-compose ps'"
echo ""
