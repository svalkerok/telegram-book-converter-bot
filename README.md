# Telegram Book Converter Bot

Минималистичный Telegram-бот для конвертации электронных книг между различными форматами.

## 🎯 Функциональность

- **Входные форматы:** PDF, EPUB, FB2, TXT, HTML
- **Выходные форматы:** PDF, EPUB, FB2, TXT, HTML, MOBI
- **Максимальный размер файла:** 50 МБ
- **Таймаут конвертации:** 60 секунд

## 🛠 Требования

- Python 3.10+
- Calibre (для ebook-convert)
- 512 МБ RAM минимум
- 1 ГБ свободного места для временных файлов

## 📦 Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd telegram-book-converter
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Установите Calibre:
```bash
# Ubuntu/Debian:
sudo apt-get install calibre

# Mac:
brew install calibre

# Или скачайте с https://calibre-ebook.com/download
```

5. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваш BOT_TOKEN
```

## 🚀 Запуск

```bash
python bot.py
```

## 📝 Структура проекта

```
telegram-book-converter/
├── bot.py               # Точка входа
├── config.py           # Конфигурация
├── handlers/
│   ├── commands.py     # Обработчики команд
│   ├── documents.py    # Обработчик файлов
│   └── callbacks.py    # Обработчик inline-кнопок
├── converter/
│   ├── converter.py    # Логика конвертации
│   └── validators.py   # Валидация файлов
├── keyboards/
│   └── inline.py       # Inline-клавиатуры
├── utils/
│   └── file_manager.py # Управление файлами
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Команды бота

- `/start` - Запуск бота и показ инструкции
- `/help` - Подробная справка о форматах и ограничениях
- `/cancel` - Отмена текущей операции

## 🎨 Примеры использования

1. Отправьте файл книги в поддерживаемом формате
2. Выберите целевой формат из предложенных кнопок
3. Дождитесь конвертации и получите результат

## 🔒 Безопасность

- Валидация размера файлов (макс. 50 МБ)
- Проверка MIME-типов
- Изоляция временных файлов
- Автоматическая очистка файлов
- Таймаут на операции конвертации

## 📄 Лицензия

MIT License
