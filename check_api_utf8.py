import requests
import json
import sys
from datetime import datetime

print('=== Проверка работы API диалогов ===')

try:
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        dialogs = response.json()
        print(f'Количество диалогов: {len(dialogs)}')
        
        if dialogs:
            first_dialog = dialogs[0]
            print(f'Первый диалог:')
            print(f'  Telegram ID: {first_dialog["telegram_id"]}')
            print(f'  Отображаемое имя: {first_dialog["display_name"]}')
            print(f'  Последнее сообщение: {first_dialog["last_message"]}')
            print(f'  Время последнего сообщения: {first_dialog["last_time"]}')
            print(f'  Непрочитанные: {first_dialog["unread_count"]}')
            
            messages_response = requests.get(
                f'http://127.0.0.1:8001/api/dialogs/{first_dialog["telegram_id"]}/messages',
                timeout=10
            )
            
            print(f'Status: {messages_response.status_code}')
            
            if messages_response.status_code == 200:
                messages_data = messages_response.json()
                if 'messages' in messages_data:
                    print(f'Количество сообщений: {len(messages_data["messages"])}')
                    for i, msg in enumerate(messages_data['messages'][:3], 1):
                        print(f'  Сообщение {i}:')
                        print(f'    Тип отправителя: {msg["sender_type"]}')
                        print(f'    Имя отправителя: {msg["sender_name"]}')
                        print(f'    Текст: {msg["content"]}')
                        print(f'    Время: {msg["created_at"]}')
                else:
                    print('Ошибка: Отсутствует поле messages')
            else:
                print(f'Ошибка: {messages_response.text}')
                
        print(f'=== Проверка отправки сообщения ===')
        if dialogs:
            first_dialog = dialogs[0]
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
                print(f'Ответ: {send_data}')
            else:
                print(f'Ошибка: {send_response.text}')
                
except Exception as e:
    print(f'Ошибка: {e}')
    print(f'Тип ошибки: {type(e)}')
    import traceback
    print(traceback.format_exc())
