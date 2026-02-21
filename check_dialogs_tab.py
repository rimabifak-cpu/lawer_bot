import requests
import json
import sys
import os

# Устанавливаем кодировку вывода
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

print('=== Проверка вкладки "Диалоги с пользователями" ===')

try:
    # Проверка API /api/dialogs
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    dialogs = response.json()
    print(f'Количество диалогов: {len(dialogs)}')
    print()
    
    for i, dialog in enumerate(dialogs, 1):
        print(f'Диалог {i}:')
        print(f'  Telegram ID: {dialog["telegram_id"]}')
        print(f'  Имя пользователя: {dialog["display_name"]}')
        print(f'  Последнее сообщение: {dialog["last_message"]}')
        print(f'  Время: {dialog["last_time"]}')
        print(f'  Непрочитанные: {dialog["unread_count"]}')
        print()
        
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
