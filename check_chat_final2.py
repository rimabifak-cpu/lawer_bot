import requests
import json
import sys
import os

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    print('=== Проверка вкладки \"Диалоги с пользователями\" ===')

    # Проверка API /api/dialogs
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    dialogs = response.json()
    print(f'Количество диалогов: {len(dialogs)}')

    for i, dialog in enumerate(dialogs, 1):
        print(f'\nДиалог {i}:')
        print(f'  Telegram ID: {dialog["telegram_id"]}')
        print(f'  Имя пользователя: {dialog["display_name"]}')
        print(f'  Последнее сообщение: {dialog["last_message"]}')
        print(f'  Время: {dialog["last_time"]}')
        print(f'  Непрочитанные: {dialog["unread_count"]}')

    # Проверка API /api/dialogs/5093303797/messages
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    data = response.json()
    print(f'\nКоличество сообщений в диалоге: {len(data.get("messages", []))}')
    
    # Показать последние 3 сообщения
    print('\nПоследние 3 сообщения:')
    for i, msg in enumerate(data.get('messages', [])[-3:], 1):
        print(f'{i}. {msg["sender_type"]}: {msg["content"]} ({msg["created_at"]})')
        
except Exception as e:
    print(f'\nОшибка: {e}')
    import traceback
    print(traceback.format_exc())
