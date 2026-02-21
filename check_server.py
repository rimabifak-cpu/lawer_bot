import requests
import time
import subprocess

# Проверка наличия процесса
try:
    result = subprocess.run(['tasklist', '/FI', 'PID eq 34696'], capture_output=True, text=True)
    print("Статус процесса 34696:")
    print(result.stdout)
except Exception as e:
    print(f"Ошибка проверки процесса: {e}")

# Проверка соединения с сервером
print("\nПроверка соединения с сервером...")
for i in range(3):
    try:
        response = requests.get('http://127.0.0.1:8001', timeout=10)
        print(f"Попытка {i+1}: статус {response.status_code}")
        if response.status_code == 200:
            print(f"Контент: {response.text[:200]}...")
        break
    except Exception as e:
        print(f"Попытка {i+1}: ошибка - {e}")
        time.sleep(2)
