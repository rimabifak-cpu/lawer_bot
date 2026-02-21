import requests
import json
import sys
import os

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    print('=== Обновление страницы и API ===')

    # Обновляем страницу
    response = requests.get('http://127.0.0.1:8001', timeout=10)
    print(f'Status: {response.status_code}')

    # Проверка API /api/dialogs
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    dialogs = response.json()
    print(f'Количество диалогов: {len(dialogs)}')

    # Проверка API /api/dialogs/5093303797/messages
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    data = response.json()
    print(f'Количество сообщений: {len(data.get("messages", []))}')

    # Показать последние 3 сообщения
    print('\nПоследние 3 сообщения:')
    for i, msg in enumerate(data.get('messages', [])[-3:], 1):
        print(f'{i}. {msg["sender_type"]}: {msg["content"]} ({msg["created_at"]})')
        
except Exception as e:
    print(f'\nОшибка: {e}')
    import traceback
    print(traceback.format_exc())
