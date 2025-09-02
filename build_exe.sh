#!/bin/bash

# 🏗️ Скрипт сборки Windows EXE файла
# Build script for Windows EXE file

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_message() {
    echo -e "${GREEN}[BUILD]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Активация виртуального окружения
activate_venv() {
    if [ -d "venv" ]; then
        print_info "Активация виртуального окружения..."
        source venv/bin/activate
        print_info "✅ Виртуальное окружение активировано"
    else
        print_error "Виртуальное окружение не найдено!"
        exit 1
    fi
}

# Проверка зависимостей
check_dependencies() {
    print_message "🔍 Проверка зависимостей..."
    
    # Проверяем PyInstaller
    if ! python -c "import PyInstaller" 2>/dev/null; then
        print_info "📦 Установка PyInstaller..."
        pip install pyinstaller
    fi
    
    # Проверяем Pillow
    if ! python -c "import PIL" 2>/dev/null; then
        print_info "📦 Установка Pillow..."
        pip install Pillow
    fi
    
    # Проверяем основные зависимости
    dependencies=("customtkinter" "requests" "dotenv" "aiofiles" "aiogram")
    imports=("customtkinter" "requests" "dotenv" "aiofiles" "aiogram")
    
    for i in "${!dependencies[@]}"; do
        dep="${dependencies[$i]}"
        imp="${imports[$i]}"
        if ! python -c "import $imp" 2>/dev/null; then
            print_error "❌ Зависимость $dep не найдена!"
            print_info "Установите: pip install $dep"
            exit 1
        fi
    done
    
    print_info "✅ Все зависимости проверены"
}

# Создание иконки
create_icon() {
    print_message "🎨 Создание иконки..."
    
    if [ ! -f "bot_icon.ico" ]; then
        python create_icon.py
    else
        print_info "✅ Иконка уже существует"
    fi
}

# Очистка предыдущих сборок
clean_build() {
    print_message "🧹 Очистка предыдущих сборок..."
    
    if [ -d "build" ]; then
        rm -rf build
        print_info "✅ Директория build очищена"
    fi
    
    if [ -d "dist" ]; then
        rm -rf dist
        print_info "✅ Директория dist очищена"
    fi
    
    if [ -f "TelegramBotGUI.exe" ]; then
        rm TelegramBotGUI.exe
        print_info "✅ Старый exe файл удален"
    fi
}

# Сборка приложения
build_exe() {
    print_message "🏗️ Сборка Windows EXE файла..."
    
    # Запускаем PyInstaller
    pyinstaller --clean bot_gui.spec
    
    if [ $? -eq 0 ]; then
        print_info "✅ Сборка завершена успешно!"
        
        # Проверяем результат (на Linux без .exe расширения)
        if [ -f "dist/TelegramBotGUI" ]; then
            # Копируем исполняемый файл в корень
            cp dist/TelegramBotGUI ./TelegramBotGUI
            
            # Создаем Windows-совместимую копию
            cp dist/TelegramBotGUI ./TelegramBotGUI.exe
            
            # Получаем размер файла
            file_size=$(du -h "TelegramBotGUI" | cut -f1)
            print_info "📦 Размер файла: $file_size"
            print_info "📁 Linux версия: $(pwd)/TelegramBotGUI"
            print_info "📁 Windows версия: $(pwd)/TelegramBotGUI.exe"
        else
            print_error "❌ Исполняемый файл не найден после сборки!"
            exit 1
        fi
    else
        print_error "❌ Ошибка при сборке!"
        exit 1
    fi
}

# Создание дистрибутива
create_distribution() {
    print_message "📦 Создание дистрибутива..."
    
    dist_dir="TelegramBotGUI_Distribution"
    
    if [ -d "$dist_dir" ]; then
        rm -rf "$dist_dir"
    fi
    
    mkdir -p "$dist_dir"
    
    # Копируем файлы
    cp TelegramBotGUI.exe "$dist_dir/"
    cp TelegramBotGUI "$dist_dir/" 2>/dev/null || true  # Копируем Linux версию если есть
    cp .env.example "$dist_dir/"
    cp README.md "$dist_dir/"
    cp GUI_GUIDE.md "$dist_dir/"
    
    # Создаем README для Windows
    cat > "$dist_dir/README_Windows.txt" << EOF
🤖 Telegram Book Converter Bot - Windows Distribution

📋 Содержимое:
- TelegramBotGUI.exe - Главное приложение
- .env.example - Пример конфигурации
- README.md - Основная документация
- GUI_GUIDE.md - Руководство по GUI

🚀 Быстрый старт:
1. Запустите TelegramBotGUI.exe
2. Введите токен бота от @BotFather
3. Нажмите "Сохранить токен"
4. Нажмите "Запустить бота"

⚠️ Требования:
- Windows 10/11
- Интернет соединение для работы бота
- Токен от @BotFather

💡 Поддержка:
- GitHub: https://github.com/svalkerok/telegram-book-converter-bot
- Документация: README.md

Версия: 1.0.0
Дата сборки: $(date)
EOF
    
    print_info "✅ Дистрибутив создан в директории: $dist_dir"
}

# Основная функция
main() {
    print_message "🏗️ Сборка Telegram Bot GUI для Windows"
    print_info "==========================================="
    
    # Проверяем что мы в правильной директории
    if [ ! -f "bot_gui.py" ]; then
        print_error "Файл bot_gui.py не найден! Запустите скрипт из директории проекта."
        exit 1
    fi
    
    # Выполняем этапы сборки
    activate_venv
    check_dependencies
    create_icon
    clean_build
    build_exe
    create_distribution
    
    print_message "🎉 Сборка завершена успешно!"
    print_info "📦 EXE файл: TelegramBotGUI.exe"
    print_info "📁 Дистрибутив: TelegramBotGUI_Distribution/"
    print_info ""
    print_info "🚀 Для запуска в Windows:"
    print_info "   1. Скопируйте папку TelegramBotGUI_Distribution на Windows"
    print_info "   2. Запустите TelegramBotGUI.exe"
    print_info "   3. Введите токен бота и наслаждайтесь!"
}

# Запуск
main "$@"
