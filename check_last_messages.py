import requests
import json
import sys
import os

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    # Проверка последних 5 сообщений в диалоге
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    data = response.json()
    
    print('=== Последние 5 сообщений ===')
    for i, msg in enumerate(data.get('messages', [])[-5:], 1):
        print(f'Сообщение {i}:')
        print(f'  Тип отправителя: {msg["sender_type"]}')
        print(f'  Имя отправителя: {msg["sender_name"]}')
        print(f'  Текст: {msg["content"]}')
        print(f'  Время: {msg["created_at"]}')
        print()
        
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
