import requests
try:
    response = requests.get('http://127.0.0.1:8001', timeout=10)
    print(f'Админ панель: статус {response.status_code}')
    print(f'Контент: {response.text[:200]}...')
except Exception as e:
    print(f'Ошибка: {e}')

try:
    response = requests.post('http://127.0.0.1:8001/api/messages/direct', 
        json={'telegram_id': 5093303797, 'content': 'Тест из Python 2'}, 
        timeout=10)
    print(f'\nAPI /api/messages/direct: статус {response.status_code}')
    print(f'Ответ: {response.text}')
except Exception as e:
    print(f'\nОшибка API: {e}')
