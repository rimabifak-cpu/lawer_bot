"""
Скрипт для ручного запуска деплоя на Render через API.
Использование: python trigger_deploy.py
"""

import os
import requests

# Замените на ваш API ключ Render (получить в Settings → API Keys)
RENDER_API_KEY = os.environ.get("RENDER_API_KEY", "")

# ID сервиса law-bot-worker (найти в URL: https://dashboard.render.com/serv-YOUR_SERVICE_ID)
SERVICE_ID = os.environ.get("RENDER_SERVICE_ID", "")

if not RENDER_API_KEY:
    print("Ошибка: RENDER_API_KEY не установлен!")
    print("Получите API ключ в Render Dashboard: Settings → API Keys")
    exit(1)

if not SERVICE_ID:
    print("Ошибка: SERVICE_ID не установлен!")
    print("Найдите ID сервиса в URL Render Dashboard")
    exit(1)

# API endpoint для деплоя
url = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys"

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "clearCache": True  # Очистить кэш перед деплоем
}

print(f"Запуск деплоя для сервиса {SERVICE_ID}...")

try:
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        deploy_info = response.json()
        print(f"✅ Деплой запущен!")
        print(f"Deploy ID: {deploy_info.get('id', 'N/A')}")
        print(f"Status: {deploy_info.get('state', 'N/A')}")
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Ошибка: {e}")
