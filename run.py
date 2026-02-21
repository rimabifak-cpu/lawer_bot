#!/usr/bin/env python3
"""
Скрипт для запуска админ панели и телеграм бота
"""

import os
import sys
import subprocess
import time

def main():
    # Путь к проекту
    project_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(project_path)

    print("=" * 50)
    print("Запуск админ панели и телеграм бота")
    print("=" * 50)
    print()

    try:
        # Запускаем админ панель
        print("1. Запускаем админ панель...")
        admin_process = subprocess.Popen([
            sys.executable, "admin_panel/app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Ожидаем запуска админ панели
        time.sleep(2)

        # Проверяем, запустилась ли админ панель
        admin_process.poll()
        if admin_process.returncode is not None:
            raise Exception(f"Админ панель не запустилась (код ошибки: {admin_process.returncode})")
        print("Админ панель запущена")

        # Запускаем телеграм бот
        print("\n2. Запускаем телеграм бот...")
        bot_process = subprocess.Popen([
            sys.executable, "run_bot.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Ожидаем запуска бота
        time.sleep(2)

        # Проверяем, запустился ли бот
        bot_process.poll()
        if bot_process.returncode is not None:
            raise Exception(f"Телеграм бот не запустился (код ошибки: {bot_process.returncode})")
        print("Телеграм бот запущен")

        print("\n" + "=" * 50)
        print("Все компоненты запущены успешно!")
        print("=" * 50)
        print(f"Админ панель доступна по адресу: http://127.0.0.1:8001")
        print(f"Логи бота и админ панели выведутся в этом окне")
        print()
        print("Нажмите Ctrl+C для остановки")

        # Подождем завершения процессов
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nЗавершение работы...")
        admin_process.terminate()
        bot_process.terminate()
        admin_process.wait()
        bot_process.wait()
        print("✅ Процессы остановлены")
    except Exception as e:
        print(f"\nОшибка: {e}")
        if 'admin_process' in locals():
            admin_process.terminate()
            admin_process.wait()
        if 'bot_process' in locals():
            bot_process.terminate()
            bot_process.wait()
        sys.exit(1)

if __name__ == "__main__":
    main()
