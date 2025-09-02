"""
🎨 Стили и темы для Bot GUI
"""

# Цветовые схемы
THEMES = {
    "blue": {
        "primary": "#1f538d",
        "secondary": "#14375e",
        "accent": "#36719f",
        "success": "#2d7d32",
        "warning": "#f57f17",
        "error": "#c62828",
        "text": "#ffffff"
    },
    "green": {
        "primary": "#2d7d32",
        "secondary": "#1b5e20",
        "accent": "#43a047",
        "success": "#388e3c",
        "warning": "#f57f17",
        "error": "#c62828",
        "text": "#ffffff"
    },
    "dark-blue": {
        "primary": "#0d1b2a",
        "secondary": "#1b263b",
        "accent": "#415a77",
        "success": "#2d7d32",
        "warning": "#f57f17",
        "error": "#c62828",
        "text": "#ffffff"
    }
}

# Размеры окон
WINDOW_SIZES = {
    "compact": "700x500",
    "normal": "800x600",
    "large": "1000x700"
}

# Шрифты
FONTS = {
    "title": ("Arial", 24, "bold"),
    "heading": ("Arial", 16, "bold"),
    "body": ("Arial", 12, "normal"),
    "code": ("Consolas", 11, "normal")
}

# Иконки (emoji)
ICONS = {
    "bot": "🤖",
    "start": "▶️",
    "stop": "⏹️",
    "restart": "🔄",
    "config": "⚙️",
    "token": "🔑",
    "save": "💾",
    "test": "🧪",
    "logs": "📋",
    "clear": "🗑️",
    "status_running": "🟢",
    "status_stopped": "🔴",
    "status_warning": "🟡",
    "eye_open": "👁️",
    "eye_closed": "🙈",
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "💡",
    "theme": "🌙",
    "sun": "🌞"
}

# Сообщения
MESSAGES = {
    "welcome": "🎉 Telegram Book Converter Bot GUI Manager запущен!",
    "token_hint": "💡 Введите токен бота и нажмите 'Сохранить токен'",
    "token_saved": "✅ Токен сохранен в конфигурации",
    "token_invalid": "❌ Токен невалиден",
    "bot_starting": "🚀 Запуск бота...",
    "bot_started": "✅ Бот успешно запущен!",
    "bot_stopping": "⏹️ Остановка бота...",
    "bot_stopped": "✅ Бот остановлен!",
    "bot_restarting": "🔄 Перезапуск бота...",
    "logs_cleared": "🗑️ Логи очищены",
    "logs_saved": "💾 Логи сохранены",
    "theme_dark": "🌙 Переключено на темную тему",
    "theme_light": "🌞 Переключено на светлую тему"
}
