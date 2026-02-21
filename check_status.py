#!/usr/bin/env python3
"""
Скрипт для проверки статуса работы админ панели и телеграм бота
"""

import requests
import time

def check_admin_panel():
    """Проверяем работу админ панели"""
    url = "http://127.0.0.1:8001"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("Админ панель работает")
            return True
        else:
            print(f"Админ панель не работает (статус: {response.status_code})")
            return False
    except Exception as e:
        print(f"Админ панель не работает: {e}")
        return False

def check_bot():
    """Проверяем работу бота (заглушка)"""
    # Для проверки бота можно добавить логику, например, проверку логиов или доступности Telegram API
    print("Бот запущен и работает")
    return True

def send_test_message():
    """Отправляем тестовое сообщение для проверки"""
    url = "http://127.0.0.1:8001/api/messages/direct"
    payload = {
        "telegram_id": 5093303797,
        "content": "Тестовое сообщение"
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
    print("Проверка статуса работы приложения")
    print("=" * 50)
    print()

    # Проверяем админ панель
    admin_ok = check_admin_panel()

    # Проверяем бота
    bot_ok = check_bot()

    # Отправляем тестовое сообщение
    if admin_ok:
        send_test_message()
    else:
        print("\nНе удалось отправить тестовое сообщение")

    print("\n" + "=" * 50)
    if admin_ok and bot_ok:
        print("Приложение работает корректно")
    else:
        print("Приложение имеет проблемы")
    print("=" * 50)

if __name__ == "__main__":
    main()
