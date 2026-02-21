import requests
import json
import sys
import os

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

print('=== Проверка вкладки \"Диалоги с пользователями\" ===')

try:
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
    
    print()
    
    # Проверка API /api/dialogs/5093303797/messages
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    data = response.json()
    print('=== Последнее сообщение в диалоге ===')
    messages = data.get('messages', [])
    
    if messages:
        last_msg = messages[-1]
        print(f'Тип отправителя: {last_msg["sender_type"]}')
        print(f'Имя отправителя: {last_msg["sender_name"]}')
        print(f'Текст: {last_msg["content"]}')
        print(f'Время: {last_msg["created_at"]}')
    else:
        print('Нет сообщений в диалоге')
        
    print()
    
    # Проверка отправки сообщения
    print('=== Проверка отправки сообщения ===')
    test_data = {
        'telegram_id': 5093303797,
        'content': 'Проверка вкладки "Диалоги с пользователями"'
    }
    
    response = requests.post('http://127.0.0.1:8001/api/messages/direct', json=test_data, timeout=10)
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print(f'Ответ: {json.dumps(result, ensure_ascii=False, indent=2)}')
        
        if result.get('sent'):
            print('✅ Сообщение отправлено успешно!')
            
            # Проверка обновления диалога
            response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
            data = response.json()
            print(f'\nКоличество сообщений в диалоге: {len(data.get("messages", []))}')
            
            last_msg = data.get('messages', [])[-1]
            print(f'Последнее сообщение:')
            print(f'  Тип отправителя: {last_msg["sender_type"]}')
            print(f'  Имя отправителя: {last_msg["sender_name"]}')
            print(f'  Текст: {last_msg["content"]}')
            print(f'  Время: {last_msg["created_at"]}')
        else:
            print('❌ Сообщение не отправлено')
    else:
        print(f'Ошибка: {response.text}')
        
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
