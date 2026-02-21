import requests

url = "http://127.0.0.1:8001/api/messages/direct"
data = {
    "telegram_id": 5093303797,
    "content": "Проверка API /api/messages/direct"
}

response = requests.post(url, json=data)

print(f"Статус код: {response.status_code}")
print(f"Ответ: {response.text}")
