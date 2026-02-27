#!/usr/bin/env python3
"""
Скрипт для запуска уведомлений через cron
"""
import asyncio
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, '/opt/law_bot')

from bot.utils.notification_sender import main

if __name__ == "__main__":
    # Получаем тип уведомлений из аргумента командной строки
    notification_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    asyncio.run(main(notification_type))
