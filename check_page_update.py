import requests
import sys
import os

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    print('=== Обновление страницы ===')
    response = requests.get('http://127.0.0.1:8001', timeout=10)
    print(f'Status: {response.status_code}')
    print(f'Content type: {response.headers.get("Content-Type")}')
    print(f'Content length: {len(response.content)} bytes')
    
    # Проверить, что содержимое страницы содержит ожидаемые элементы
    content = response.text
    if 'Admin Panel' in content and 'Диалоги с пользователями' in content:
        print('✅ Страница загружена корректно')
    else:
        print('❌ Страница не содержит ожидаемых элементов')
        
except Exception as e:
    print(f'Ошибка: {e}')
    import traceback
    print(traceback.format_exc())
