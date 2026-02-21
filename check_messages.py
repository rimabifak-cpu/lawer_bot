import requests

url = "http://127.0.0.1:8001/api/dialogs/5093303797/messages"
response = requests.get(url)

print(f"Статус код: {response.status_code}")
print(f"Ответ: {response.text}")
