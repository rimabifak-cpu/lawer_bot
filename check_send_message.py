import requests
import json
import sys
import os

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

print('=== Проверка отправки сообщения ===')

try:
    data = {
        'telegram_id': 5093303797,
        'content': 'Тестовое сообщение через API'
    }

    response = requests.post('http://127.0.0.1:8001/api/messages/direct', json=data, timeout=10)
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print(f'Response: {json.dumps(result, ensure_ascii=False, indent=2)}')
        
        if result.get('sent'):
            print('✅ Сообщение отправлено успешно!')
        else:
            print('❌ Сообщение не отправлено')
            
    else:
        print(f'Ошибка: {response.text}')
        
    print()
    
    # Проверка обновления диалога
    print('=== Проверка обновления диалога ===')
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    dialogs = response.json()
    print(f'Количество диалогов: {len(dialogs)}')
    
    for dialog in dialogs:
        print(f'Последнее сообщение: {dialog["last_message"]}')
        print(f'Время: {dialog["last_time"]}')
        
    print()
    
    # Проверка количества сообщений
    print('=== Проверка количества сообщений ===')
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    data = response.json()
    print(f'Количество сообщений: {len(data.get("messages", []))}')
        
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
