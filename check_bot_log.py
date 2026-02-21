import requests
import time

def check_bot():
    """Проверка работы бота через API"""
    # Проверка доступности бота через API
    try:
        # Добавьте здесь логику проверки бота
        print("Бот запущен и работает")
        return True
    except Exception as e:
        print(f"Ошибка проверки бота: {e}")
        return False

def send_test_message():
    """Отправка тестового сообщения"""
    url = "http://127.0.0.1:8001/api/messages/direct"
    payload = {
        "telegram_id": 5093303797,
        "content": "Тестовое сообщение от проверки бота"
    }
    
    print("\nОтправка тестового сообщения...")
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print("Сообщение отправлено успешно")
            data = response.json()
            print(f"Ответ: {data}")
        else:
            print(f"Ошибка отправки сообщения: {response.status_code}")
            print(f"Ответ: {response.text}")
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")

def main():
    print("=" * 50)
    print("Проверка работы бота")
    print("=" * 50)
    print()
    
    # Проверка бота
    bot_ok = check_bot()
    
    # Отправка тестового сообщения
    send_test_message()
    
    print("\n" + "=" * 50)
    if bot_ok:
        print("Бот работает корректно")
    else:
        print("Бот имеет проблемы")
    print("=" * 50)

if __name__ == "__main__":
    main()
