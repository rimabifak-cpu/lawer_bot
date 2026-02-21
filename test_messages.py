import requests
try:
    response = requests.get('http://127.0.0.1:8001/api/dialogs/5093303797/messages', timeout=10)
    print(f'Сообщения: статус {response.status_code}')
    print(f'Ответ: {response.text}')
except Exception as e:
    print(f'Ошибка сообщений: {e}')
