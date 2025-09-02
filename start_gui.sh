#!/bin/bash

# 🎨 Скрипт запуска GUI для Telegram Book Converter Bot
# GUI Launch Script for Telegram Book Converter Bot

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_message() {
    echo -e "${GREEN}[GUI]${NC} $1"
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

# Функция для проверки зависимостей
check_dependencies() {
    print_message "🔍 Проверка зависимостей..."
    
    # Проверяем Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 не найден. Установите Python 3.8+"
        exit 1
    fi
    
    # Проверяем pip
    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        print_error "pip не найден. Установите pip"
        exit 1
    fi
    
    # Используем правильную команду pip
    PIP_CMD="pip3"
    if command -v pip &> /dev/null; then
        PIP_CMD="pip"
    fi
    
    print_info "✅ Python найден: $(python3 --version)"
    print_info "✅ pip найден: $($PIP_CMD --version | cut -d' ' -f1-2)"
}

# Функция для установки зависимостей
install_dependencies() {
    print_message "📦 Установка зависимостей GUI..."
    
    # Проверяем и устанавливаем customtkinter
    if ! python3 -c "import customtkinter" &> /dev/null; then
        print_info "🔧 Установка CustomTkinter..."
        $PIP_CMD install customtkinter==5.2.2
    else
        print_info "✅ CustomTkinter уже установлен"
    fi
    
    # Проверяем и устанавливаем requests
    if ! python3 -c "import requests" &> /dev/null; then
        print_info "🔧 Установка requests..."
        $PIP_CMD install requests==2.32.5
    else
        print_info "✅ requests уже установлен"
    fi
    
    # Проверяем tkinter (обычно идет с Python)
    if ! python3 -c "import tkinter" &> /dev/null; then
        print_warning "❌ tkinter не найден. На Ubuntu/Debian выполните:"
        print_info "sudo apt-get install python3-tk"
        exit 1
    else
        print_info "✅ tkinter доступен"
    fi
}

# Функция для проверки файлов проекта
check_project_files() {
    print_message "📁 Проверка файлов проекта..."
    
    local required_files=("bot_gui.py" "gui_styles.py" "bot.py")
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "❌ Отсутствуют обязательные файлы:"
        for file in "${missing_files[@]}"; do
            print_error "   - $file"
        done
        exit 1
    fi
    
    print_info "✅ Все файлы проекта найдены"
}

# Функция для запуска GUI
launch_gui() {
    print_message "🚀 Запуск GUI интерфейса..."
    
    # Устанавливаем переменные окружения для лучшей работы tkinter
    export DISPLAY=${DISPLAY:-:0}
    
    # Запускаем GUI
    python3 bot_gui.py
}

# Функция для показа помощи
show_help() {
    echo "🤖 Telegram Book Converter Bot - GUI Manager"
    echo ""
    echo "Использование: $0 [ОПЦИИ]"
    echo ""
    echo "Опции:"
    echo "  -h, --help              Показать эту справку"
    echo "  -c, --check-only        Только проверить зависимости"
    echo "  --install-deps          Принудительно переустановить зависимости"
    echo "  --debug                 Запуск в режиме отладки"
    echo ""
    echo "Примеры:"
    echo "  $0                      Запустить GUI"
    echo "  $0 --check-only         Проверить готовность к запуску"
    echo "  $0 --install-deps       Переустановить зависимости"
    echo ""
}

# Основная логика
main() {
    local check_only=false
    local install_deps=false
    local debug=false
    
    # Обработка аргументов командной строки
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--check-only)
                check_only=true
                shift
                ;;
            --install-deps)
                install_deps=true
                shift
                ;;
            --debug)
                debug=true
                shift
                ;;
            *)
                print_error "Неизвестная опция: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Устанавливаем режим отладки
    if [[ "$debug" == true ]]; then
        set -x
        export DEBUG=1
    fi
    
    print_message "🎨 Telegram Book Converter Bot - GUI Manager"
    print_info "============================================"
    
    # Проверяем зависимости
    check_dependencies
    
    # Принудительная установка зависимостей
    if [[ "$install_deps" == true ]]; then
        install_dependencies
    fi
    
    # Проверяем файлы проекта
    check_project_files
    
    # Если только проверка - выходим
    if [[ "$check_only" == true ]]; then
        print_message "✅ Все проверки пройдены! GUI готов к запуску."
        exit 0
    fi
    
    # Устанавливаем зависимости если нужно
    if [[ "$install_deps" != true ]]; then
        install_dependencies
    fi
    
    # Запускаем GUI
    launch_gui
}

# Обработка сигналов
trap 'print_warning "🛑 Получен сигнал прерывания. Завершение работы..."; exit 130' INT TERM

# Запуск
main "$@"
