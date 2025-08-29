# 📚 Telegram Book Converter Bot

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![aiogram](https://img.shields.io/badge/aiogram-v3.13+-green.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Универсальный Telegram бот для конвертации электронных книг между различными форматами. Поддерживает более 20 форматов книг и работает на основе библиотеки Calibre.

## ✨ Возможности

- 📖 **20+ форматов книг**: PDF, EPUB, MOBI, FB2, TXT, HTML, RTF, DOC, DOCX и другие
- 🔄 **Быстрая конвертация**: Использует мощный движок Calibre
- 🛡️ **Безопасность**: Валидация файлов, ограничения размера
- 🐳 **Docker ready**: Готов к развертыванию в контейнерах
- ⚡ **Простой интерфейс**: Интуитивные inline-клавиатуры
- 📊 **Мониторинг**: Логирование и health checks
- 🔧 **Продакшен готов**: Настройки для серверного развертывания

## 🚀 Быстрый старт

### Локальная разработка

```bash
# Клонируйте репозиторий
git clone https://github.com/YOUR_USERNAME/telegram-book-converter.git
cd telegram-book-converter

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Установите Calibre
sudo apt install calibre  # Ubuntu/Debian
brew install calibre      # macOS

# Настройте бота
cp .env.example .env
# Отредактируйте .env и добавьте ваш BOT_TOKEN

# Запустите бота
python bot.py
```

### Docker развертывание

```bash
# Клонируйте и настройте
git clone https://github.com/YOUR_USERNAME/telegram-book-converter.git
cd telegram-book-converter
cp .env.example .env
# Добавьте BOT_TOKEN в .env

# Запустите через Docker
docker-compose up -d --build
```

## 📦 Развертывание на сервере

### Hetzner Cloud / VPS

```bash
# Автоматический деплой
./deploy.sh YOUR_SERVER_IP root YOUR_BOT_TOKEN

# Или следуйте подробной инструкции
cat DEPLOY.md
```

### Systemd service

```bash
# Установка как системный сервис
sudo cp telegram-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## 🔧 Конфигурация

### Основные настройки

```bash
# .env файл
BOT_TOKEN=your_bot_token_here
PRODUCTION=1                    # Режим продакшена
LOG_LEVEL=INFO                 # Уровень логирования
CONVERSION_TIMEOUT=300         # Таймаут конвертации (сек)
MAX_FILE_SIZE=52428800        # Максимальный размер файла (50MB)
```

### Поддерживаемые форматы

**Входные форматы:**
- Документы: PDF, DOC, DOCX, RTF, TXT, HTML
- Электронные книги: EPUB, MOBI, AZW, AZW3, FB2
- И многие другие...

**Выходные форматы:**
- EPUB, PDF, MOBI, FB2, TXT, HTML, RTF, DOCX

## 🏗️ Архитектура

```
telegram-book-converter/
├── bot.py                 # Главный файл
├── config.py             # Конфигурация
├── handlers/             # Обработчики Telegram
│   ├── commands.py       # Команды (/start, /help)
│   ├── documents.py      # Обработка файлов
│   └── callbacks.py      # Inline-кнопки
├── converter/            # Модуль конвертации
│   ├── converter.py      # Логика конвертации
│   └── validators.py     # Валидация файлов
├── keyboards/            # UI элементы
│   └── inline.py         # Клавиатуры
├── utils/                # Утилиты
│   └── file_manager.py   # Управление файлами
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker оркестрация
└── deploy.sh            # Скрипт деплоя
```

## 📊 Мониторинг

```bash
# Проверка здоровья
python health_check.py

# Логи Docker
docker-compose logs -f telegram-bot

# Логи systemd
journalctl -u telegram-bot -f

# Статус ресурсов
docker stats telegram-book-converter
```

## 🛠️ Разработка

### Требования

- Python 3.12+
- aiogram 3.13+
- Calibre
- Docker (опционально)

### Тестирование

```bash
# Тест конвертера
python test_converter.py

# Проверка готовности к деплою
./check_deploy.sh
```

### Структура кода

```python
# Пример использования конвертера
from converter.converter import BookConverter
from pathlib import Path

converter = BookConverter()
result = await converter.convert(
    input_path=Path("book.pdf"),
    output_format="epub"
)
```

## 🔐 Безопасность

- ✅ Валидация типов файлов
- ✅ Ограничения размера файлов
- ✅ Временные файлы автоматически удаляются
- ✅ Непривилегированный пользователь в Docker
- ✅ Ограничения ресурсов

## 📝 Лицензия

MIT License - см. [LICENSE](LICENSE) файл.

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📞 Поддержка

- 📋 **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/telegram-book-converter/issues)
- 📧 **Email**: your.email@example.com
- 💬 **Telegram**: @your_username

## 🙏 Благодарности

- [aiogram](https://github.com/aiogram/aiogram) - Современный фреймворк для Telegram Bot API
- [Calibre](https://calibre-ebook.com/) - Мощная библиотека для работы с электронными книгами
- [Python](https://python.org/) - Язык программирования

---

⭐ **Понравился проект? Поставьте звездочку!**
