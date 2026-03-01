#!/bin/bash
# Скрипт для исправления админки на сервере

cd /law_bot || exit 1

# Исправляем проблемную строку в app.py
# Удаляем лишний await db.commit() из блока else
sed -i '1224d' admin_panel/app.py

# Пересобираем и перезапускаем админку
docker-compose build admin
docker-compose up -d admin

# Проверяем логи
docker-compose logs --tail=50 admin
