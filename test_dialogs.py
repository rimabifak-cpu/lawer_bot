import requests
try:
    response = requests.get('http://127.0.0.1:8001/api/dialogs', timeout=10)
    print(f'Диалоги: статус {response.status_code}')
    print(f'Ответ: {response.text}')
except Exception as e:
    print(f'Ошибка диалогов: {e}')
