# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    calibre \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash botuser

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем директорию для временных файлов
RUN mkdir -p /app/temp && chown -R botuser:botuser /app

# Переключаемся на непривилегированного пользователя
USER botuser

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Открываем порт (если нужен для webhooks)
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "bot.py"]
