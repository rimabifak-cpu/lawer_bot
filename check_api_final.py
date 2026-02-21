import requests
import json
import sys
import os

# Устанавливаем кодировку вывода
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

print('=== Проверка финальной работы API ===')

try:
    # Проверка API /api/dialogs
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    print(f'API /api/dialogs status: {response.status_code}')
    dialogs = response.json()
    print(f'Response type: {type(dialogs)}')
    print(f'Содержимое:')
    print(json.dumps(dialogs, ensure_ascii=False, indent=2))
    print()
    
    # Проверка API /api/dialogs/5093303797/messages
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    print(f'API /api/dialogs/5093303797/messages status: {response.status_code}')
    data = response.json()
    print(f'Messages count: {len(data.get("messages", []))}')
    print('Содержимое:')
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
