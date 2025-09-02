#!/bin/bash

# 🔄 Скрипт обновления и пересборки приложения
# Используется для быстрого обновления исполняемых файлов после изменений

set -e  # Остановка при любой ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Telegram Bot GUI - Скрипт обновления${NC}"
echo "=================================="

# Функция логирования
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] ⚠️  $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ❌ $1${NC}"
}

# Проверка виртуального окружения
if [[ "$VIRTUAL_ENV" == "" ]]; then
    warn "Виртуальное окружение не активировано!"
    echo "Пытаюсь активировать venv..."
    
    if [ -d "venv" ]; then
        source venv/bin/activate
        log "Виртуальное окружение активировано"
    else
        error "Папка venv не найдена! Создайте виртуальное окружение:"
        echo "python -m venv venv"
        echo "source venv/bin/activate"
        exit 1
    fi
fi

# Проверка изменений в Git (если это Git репозиторий)
if [ -d ".git" ]; then
    if ! git diff --quiet; then
        warn "Есть несохраненные изменения в Git"
        echo "Файлы с изменениями:"
        git diff --name-only
        echo ""
        read -p "Продолжить сборку? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Сборка отменена"
            exit 1
        fi
    fi
fi

# Обновление зависимостей
log "Проверка зависимостей..."
pip install --upgrade pyinstaller Pillow customtkinter requests python-dotenv

# Создание резервной копии текущего дистрибутива
if [ -d "TelegramBotGUI_Distribution" ]; then
    log "Создание резервной копии..."
    timestamp=$(date +"%Y%m%d_%H%M%S")
    mv TelegramBotGUI_Distribution TelegramBotGUI_Distribution_backup_$timestamp
    log "Резервная копия: TelegramBotGUI_Distribution_backup_$timestamp"
fi

if [ -f "TelegramBotGUI_Windows.zip" ]; then
    mv TelegramBotGUI_Windows.zip TelegramBotGUI_Windows_backup_$timestamp.zip
fi

# Очистка старых файлов сборки
log "Очистка старых файлов сборки..."
rm -rf build dist __pycache__ *.pyc

# Пересоздание иконки (на случай если она изменилась)
log "Обновление иконки..."
python create_icon.py

# Основная сборка
log "Запуск основной сборки..."
./build_exe.sh

# Проверка результатов
if [ -f "dist/TelegramBotGUI.exe" ] && [ -f "dist/TelegramBotGUI" ]; then
    log "✅ Сборка успешно завершена!"
    
    # Размеры файлов
    echo ""
    echo "📊 Размеры файлов:"
    echo "Windows EXE: $(du -h dist/TelegramBotGUI.exe | cut -f1)"
    echo "Linux Binary: $(du -h dist/TelegramBotGUI | cut -f1)"
    
    if [ -f "TelegramBotGUI_Windows.zip" ]; then
        echo "ZIP архив: $(du -h TelegramBotGUI_Windows.zip | cut -f1)"
    fi
    
    echo ""
    log "Дистрибутив готов в папке: TelegramBotGUI_Distribution/"
    
    # Быстрый тест запуска (для Linux версии)
    echo ""
    read -p "Протестировать Linux версию? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "Запуск тестирования..."
        timeout 5s ./dist/TelegramBotGUI || true
        log "Тест завершен (окно закрыто через 5 сек)"
    fi
    
else
    error "Сборка не удалась! Проверьте логи выше."
    exit 1
fi

# Удаление старых резервных копий (больше 7 дней)
log "Очистка старых резервных копий..."
find . -name "TelegramBotGUI_Distribution_backup_*" -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null || true
find . -name "TelegramBotGUI_Windows_backup_*.zip" -type f -mtime +7 -delete 2>/dev/null || true

echo ""
echo -e "${GREEN}🎉 Обновление завершено успешно!${NC}"
echo ""
echo "📁 Готовые файлы:"
echo "   • TelegramBotGUI_Distribution/ - Папка дистрибутива"
echo "   • TelegramBotGUI_Windows.zip - ZIP архив для Windows"
echo ""
echo "🚀 Следующие шаги:"
echo "   • Протестируйте приложения на целевых системах"
echo "   • Распространите TelegramBotGUI_Windows.zip для Windows пользователей"
echo "   • Используйте TelegramBotGUI_Distribution/TelegramBotGUI для Linux"
echo ""
