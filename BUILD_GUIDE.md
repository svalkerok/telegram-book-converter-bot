# 🏗️ Сборка исполняемых файлов

## 📋 Обзор

Проект поддерживает создание исполняемых файлов для различных платформ:
- 🐧 **Linux** - нативная сборка
- 🪟 **Windows** - кросс-платформенная сборка
- 🍎 **macOS** - потенциальная поддержка

## 🛠️ Инструменты сборки

### Основные компоненты
- **PyInstaller** - создание исполняемых файлов
- **Pillow** - генерация иконок
- **CustomTkinter** - GUI фреймворк
- **Bash скрипты** - автоматизация процесса

### Файлы конфигурации
- `bot_gui.spec` - конфигурация PyInstaller
- `version_info.txt` - информация о версии для Windows
- `build_exe.sh` - скрипт автоматической сборки

## 🚀 Быстрая сборка

```bash
# Автоматическая сборка
./build_exe.sh

# Результат:
# - TelegramBotGUI (Linux)
# - TelegramBotGUI.exe (Windows совместимый)
# - TelegramBotGUI_Distribution/ (дистрибутив)
# - TelegramBotGUI_Windows.zip (архив для Windows)
```

## 📦 Ручная сборка

### 1. Подготовка окружения

```bash
# Активация виртуального окружения
source venv/bin/activate

# Установка инструментов сборки
pip install pyinstaller Pillow

# Создание иконки
python create_icon.py
```

### 2. Конфигурация PyInstaller

```bash
# Редактирование bot_gui.spec для настройки:
# - Путей к файлам
# - Скрытых импортов
# - Исключений
# - Иконки и версии
```

### 3. Сборка

```bash
# Очистка предыдущих сборок
rm -rf build dist

# Сборка через spec файл
pyinstaller --clean bot_gui.spec

# Результат в папке dist/
```

## 🎯 Структура дистрибутива

```
TelegramBotGUI_Distribution/
├── TelegramBotGUI.exe          # Главное приложение (Windows)
├── TelegramBotGUI              # Приложение для Linux
├── start.bat                   # Батч-файл для Windows
├── .env.example                # Пример конфигурации
├── README.md                   # Основная документация
├── GUI_GUIDE.md                # Руководство по GUI
├── WINDOWS_SETUP.md            # Инструкции для Windows
└── README_Windows.txt          # Краткая справка
```

## 🔧 Настройка для различных платформ

### Windows
```python
# В bot_gui.spec
exe = EXE(
    # ...
    console=False,              # Без консоли
    icon='bot_icon.ico',        # Иконка
    version='version_info.txt'  # Информация о версии
)
```

### Linux
```python
# Автоматически определяется PyInstaller
# Результат: исполняемый файл без расширения
```

### macOS (потенциально)
```python
# Требует изменений в spec файле:
app = BUNDLE(exe,
    name='TelegramBotGUI.app',
    icon='bot_icon.icns',       # Формат ICNS для macOS
    bundle_identifier='com.telegram.botgui'
)
```

## 🐛 Устранение неполадок

### Отсутствующие зависимости
```bash
# Добавьте в hiddenimports в bot_gui.spec:
hiddenimports = [
    'customtkinter',
    'tkinter',
    'requests',
    'dotenv',  # Не python-dotenv!
    # ... другие модули
]
```

### Размер файла
```bash
# Текущий размер: ~15MB
# Для уменьшения:
# 1. Добавьте в excludes ненужные модули
# 2. Используйте UPX сжатие
# 3. Исключите документацию и примеры
```

### Проблемы с иконкой
```bash
# Linux/macOS игнорируют Windows иконки
# Создайте отдельные иконки для каждой платформы
# Или используйте простые PNG файлы
```

## 📊 Характеристики сборки

| Параметр | Значение |
|----------|----------|
| Размер | ~15 MB |
| Время сборки | ~30 сек |
| Поддерживаемые ОС | Linux, Windows |
| Зависимости | Включены |
| GUI | CustomTkinter |
| Иконка | Включена |

## 🔄 Автоматизация

### CI/CD интеграция
```yaml
# GitHub Actions example
name: Build Executables
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller Pillow
      - name: Build executable
        run: ./build_exe.sh
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: TelegramBotGUI
          path: TelegramBotGUI_Windows.zip
```

## 📚 Дополнительные ресурсы

- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [CustomTkinter Packaging](https://customtkinter.tomschimansky.com/documentation/packaging)
- [Cross-platform Python Apps](https://realpython.com/pyinstaller-python/)

---

**Поддерживаемые платформы**: Linux ✅, Windows ✅, macOS 🔄  
**Последнее обновление**: $(date)
