      1 # Lawer Bot - Деплой и Обновление
      2
      3 ## 📋 Информация о сервере
      4
      5 | Параметр | Значение |
      6 |----------|----------|
      7 | **IP сервера** | 195.133.31.34 |
      8 | **Пользователь** | root |
      9 | **Директория проекта** | /opt/law_bot |
     10 | **Бот Telegram** | @legaldecision_bot (ID: 8429912645) |
     11 | **Админ-панель** | http://195.133.31.34:8000 |
     12
     13 ---
     14
     15 ## 🚀 Инструкция по обновлению проекта
    cd /opt/law_bot
    git fetch origin
    git checkout main
    git pull origin main
    /usr/local/bin/docker-compose down
    /usr/local/bin/docker-compose up -d --build
    /usr/local/bin/docker-compose logs -f bot

      1
      2 ---
      3
      4 ## 💾 Сохранение данных
      5
      6 ### Что сохраняется:
      7 - postgres_data — База данных
      8 - ./uploads — Загруженные файлы
      9 - ./logs — Логи
     10
     11 ### ⚠️ ОПАСНЫЕ команды (данные будут УДАЛЕНЫ):
     12 - docker-compose down -v
     13 - docker volume rm law_bot_postgres_data
     14 - rm -rf /opt/law_bot/uploads
     15
     16 ### ✅ Безопасные команды:
     17 - git pull
     18 - docker-compose up -d --build
     19 - docker-compose restart
     20 - docker-compose down (без -v!)
     21
     22 ---
     23
     24 ## 🔧 Решение проблем
    Проверить логи
    docker-compose logs bot --tail=50

    Проверить БД
    docker exec law_bot_db psql -U law_bot_user -d law_bot_db -c "SELECT COUNT(*) FROM users;"

     1
     2 ---
     3
     4 Последнее обновление: 27.02.2026
