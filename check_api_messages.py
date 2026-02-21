import requests
import json
from datetime import datetime
import sys
import os

# Устанавливаем кодировку вывода
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

print('=== Проверка диалога пользователя ===')
try:
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'Пользователь: {data.get("user_name")}')
        print(f'Количество сообщений: {len(data.get("messages", []))}')
        
        # Показать последние 5 сообщений
        messages = data.get('messages', [])
        for i, msg in enumerate(messages[-5:], 1):
            print(f'Сообщение {i}:')
            print(f'  Тип: {msg["sender_type"]}')
            print(f'  Отправитель: {msg["sender_name"]}')
            print(f'  Текст: {msg["content"]}')
            print(f'  Время: {datetime.fromisoformat(msg["created_at"])}')
            print()
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
