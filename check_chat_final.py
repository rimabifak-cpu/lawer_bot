import requests
import json
import sys
import os

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    # Проверка API /api/dialogs
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    dialogs = response.json()
    print('=== Диалоги ===')
    for dialog in dialogs:
        print(f'Telegram ID: {dialog["telegram_id"]}')
        print(f'Имя: {dialog["display_name"]}')
        print(f'Последнее сообщение: {dialog["last_message"]}')
        print(f'Время: {dialog["last_time"]}')
        print(f'Непрочитанные: {dialog["unread_count"]}')
        print()

    # Проверка сообщений в диалоге
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    data = response.json()
    print('=== Сообщения ===')
    print(f'Количество сообщений: {len(data.get("messages", []))}')
    for msg in data.get('messages', [])[-3:]:
        print(f'{msg["sender_type"]}: {msg["content"]} ({msg["created_at"]})')
        
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
