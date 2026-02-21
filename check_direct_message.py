import requests
import json
import sys

print('=== Проверка отправки сообщения ===')

try:
    # Проверка списка диалогов
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    dialogs = response.json()
    
    if dialogs:
        first_dialog = dialogs[0]
        print(f'Отправка сообщения пользователю: {first_dialog["display_name"]}')
        print(f'Telegram ID: {first_dialog["telegram_id"]}')
        
        test_message = {
            'telegram_id': first_dialog['telegram_id'],
            'content': 'Тестовое сообщение через API'
        }
        
        send_response = requests.post(
            'http://127.0.0.1:8001/api/messages/direct',
            json=test_message,
            timeout=10
        )
        
        print(f'Status: {send_response.status_code}')
        
        if send_response.status_code == 200:
            send_data = send_response.json()
            print(f'Ответ: {json.dumps(send_data, ensure_ascii=False)}')
        else:
            print(f'Ошибка: {send_response.text}')
            
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
