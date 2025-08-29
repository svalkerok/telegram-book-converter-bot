# 🚀 Деплой на Hetzner.com

## 🏗️ Подготовка к деплою

### 1. Требования к серверу
- **ОС**: Ubuntu 20.04+ / Debian 11+
- **RAM**: минимум 1GB, рекомендуется 2GB
- **Диск**: минимум 10GB свободного места
- **CPU**: 1+ ядра

### 2. Настройка сервера Hetzner

1. **Создайте сервер** в панели Hetzner Cloud
2. **Подключитесь по SSH**:
   ```bash
   ssh root@YOUR_SERVER_IP
   ```

3. **Обновите систему**:
   ```bash
   apt update && apt upgrade -y
   ```

## 🐳 Метод 1: Docker деплой (рекомендуется)

### Автоматический деплой
```bash
./deploy.sh YOUR_SERVER_IP root YOUR_BOT_TOKEN
```

### Ручной деплой
```bash
# На сервере
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Создайте директорию
mkdir -p /opt/telegram-bot
cd /opt/telegram-bot

# Загрузите файлы проекта (через scp или git)
# Создайте .env
echo "BOT_TOKEN=YOUR_BOT_TOKEN" > .env
echo "PRODUCTION=1" >> .env

# Запустите
docker-compose up -d
```

## 🔧 Метод 2: Systemd service

### 1. Подготовка сервера
```bash
# Установка Python и зависимостей
apt install -y python3 python3-pip python3-venv calibre

# Создание пользователя
useradd --create-home --shell /bin/bash botuser

# Создание директории
mkdir -p /opt/telegram-bot
chown botuser:botuser /opt/telegram-bot
```

### 2. Установка бота
```bash
# Как пользователь botuser
su - botuser
cd /opt/telegram-bot

# Загрузите файлы проекта
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка
echo "BOT_TOKEN=YOUR_BOT_TOKEN" > .env
echo "PRODUCTION=1" >> .env
```

### 3. Установка сервиса
```bash
# Как root
cp /opt/telegram-bot/telegram-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
```

## 📊 Мониторинг

### Проверка статуса (Docker)
```bash
cd /opt/telegram-bot
docker-compose logs -f
docker-compose ps
```

### Проверка статуса (Systemd)
```bash
systemctl status telegram-bot
journalctl -u telegram-bot -f
```

### Health check
```bash
cd /opt/telegram-bot
python3 health_check.py
```

## 🔐 Безопасность

### 1. Настройка файрвола
```bash
ufw enable
ufw allow ssh
ufw allow from YOUR_IP  # Ограничить SSH доступ
```

### 2. Регулярные обновления
```bash
# Создайте cron задачу для обновлений
echo "0 2 * * * apt update && apt upgrade -y" | crontab -
```

### 3. Бэкапы логов
```bash
# Настройка logrotate
cat > /etc/logrotate.d/telegram-bot << EOF
/opt/telegram-bot/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
```

## 🚨 Troubleshooting

### Проблемы с запуском
```bash
# Проверка логов
docker-compose logs telegram-bot
# или
journalctl -u telegram-bot --no-pager

# Проверка конфигурации
cat /opt/telegram-bot/.env

# Проверка Calibre
ebook-convert --version
```

### Проблемы с конвертацией
```bash
# Проверка свободного места
df -h

# Проверка прав доступа
ls -la /opt/telegram-bot/temp/
```

### Перезапуск бота
```bash
# Docker
docker-compose restart

# Systemd
systemctl restart telegram-bot
```

## 📈 Оптимизация

### 1. Настройка лимитов
В `docker-compose.yml` или systemd service уже настроены ограничения ресурсов.

### 2. Мониторинг ресурсов
```bash
# Использование CPU/RAM
htop
# или
docker stats telegram-book-converter
```

### 3. Очистка временных файлов
```bash
# Создайте cron задачу
echo "0 1 * * * find /opt/telegram-bot/temp -type f -mtime +1 -delete" | crontab -
```

## 🔄 Обновление бота

### Docker
```bash
cd /opt/telegram-bot
docker-compose down
# Загрузите новые файлы
docker-compose build
docker-compose up -d
```

### Systemd
```bash
systemctl stop telegram-bot
# Обновите файлы
systemctl start telegram-bot
```

## 📞 Поддержка

При проблемах проверьте:
1. Логи бота
2. Статус сервисов
3. Свободное место на диске
4. Работоспособность Calibre
5. Корректность BOT_TOKEN
