FROM python:3.11-slim

# Устанавливаем системные зависимости включая Ghostscript для оптимизации PDF
RUN apt-get update && apt-get install -y \
    calibre \
    ghostscript \
    fonts-liberation \
    fonts-dejavu \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash botuser

# Настраиваем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем директории для временных файлов и настраиваем права
RUN mkdir -p /app/temp && chown -R botuser:botuser /app

# Переключаемся на пользователя botuser
USER botuser

# Настраиваем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Порт для health check
EXPOSE 8000

# Запускаем бота
CMD ["python", "bot.py"]
