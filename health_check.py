#!/usr/bin/env python3
"""
Health check скрипт для мониторинга состояния бота.
"""
import asyncio
import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Добавляем путь к проекту
sys.path.append('/opt/telegram-bot')

async def health_check():
    """Проверка состояния бота"""
    try:
        # Проверяем конфигурацию
        from config import BOT_TOKEN
        if not BOT_TOKEN:
            raise ValueError("BOT_TOKEN not configured")
        
        # Проверяем доступность Calibre
        import subprocess
        result = subprocess.run(['ebook-convert', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            raise Exception("Calibre not available")
        
        # Проверяем директории
        temp_dir = Path('/opt/telegram-bot/temp')
        logs_dir = Path('/opt/telegram-bot/logs')
        
        if not temp_dir.exists():
            temp_dir.mkdir(parents=True)
        if not logs_dir.exists():
            logs_dir.mkdir(parents=True)
        
        # Проверяем свободное место
        import shutil
        total, used, free = shutil.disk_usage('/opt/telegram-bot')
        free_gb = free // (1024**3)
        
        if free_gb < 1:  # Меньше 1GB свободного места
            raise Exception(f"Low disk space: {free_gb}GB free")
        
        print(f"✅ Health check passed at {datetime.now()}")
        print(f"📁 Free disk space: {free_gb}GB")
        print(f"🔧 Calibre version: {result.stdout.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(health_check())
    sys.exit(0 if success else 1)
