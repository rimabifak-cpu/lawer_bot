# Деплой телеграм бота

## Подготовка к деплою

Перед деплоем необходимо подготовить сервер или облачную платформу для запуска приложения.

## Требования к серверу

- Python 3.9+
- PostgreSQL (или другой поддерживаемый тип базы данных)
- pip (для установки зависимостей)

## Шаги для деплоя

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd law_bot
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_CHAT_ID=your_admin_chat_id
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=20971520
DEBUG=False
```

### 4. Настройка базы данных

Создайте базу данных PostgreSQL и обновите строку подключения в переменной `DATABASE_URL`.

### 5. Запуск бота

Для запуска бота используйте команду:

```bash
python -m bot.main
```

### 6. Запуск админ-панели

Для запуска админ-панели:

```bash
cd admin_panel
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Деплой на VPS

### Установка systemd сервисов

Создайте файл `/etc/systemd/system/law_bot.service`:

```ini
[Unit]
Description=Law Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/law_bot
ExecStart=/usr/bin/python3 -m bot.main
Restart=always
EnvironmentFile=/path/to/law_bot/.env

[Install]
WantedBy=multi-user.target
```

Создайте файл `/etc/systemd/system/law_admin.service`:

```ini
[Unit]
Description=Law Admin Panel
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/law_bot/admin_panel
ExecStart=/usr/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
EnvironmentFile=/path/to/law_bot/.env

[Install]
WantedBy=multi-user.target
```

Запустите и включите сервисы:

```bash
sudo systemctl daemon-reload
sudo systemctl start law_bot
sudo systemctl enable law_bot
sudo systemctl start law_admin
sudo systemctl enable law_admin
```

## Деплой на Heroku

1. Установите Heroku CLI
2. Авторизуйтесь: `heroku login`
3. Создайте приложение: `heroku create your-app-name`
4. Добавьте buildpack для Python: `heroku buildpacks:set heroku/python`
5. Установите переменные окружения: `heroku config:set BOT_TOKEN=your_token ...`
6. Запушьте код: `git push heroku main`

## Деплой на Docker

Создайте Dockerfile:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "bot.main"]
```

Создайте docker-compose.yml:

```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file:
      - .env
    volumes:
      - ./uploads:/app/uploads
    restart: always
  
  admin:
    build: .
    command: uvicorn admin_panel.app:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./uploads:/app/uploads
    restart: always
```

Запустите: `docker-compose up -d`

## Мониторинг и логирование

Для мониторинга состояния бота можно использовать стандартные логи Linux:

```bash
sudo journalctl -u law_bot -f
```

Или для Docker:

```bash
docker logs -f law_bot_container
```

## Обновление приложения

1. Остановите сервис: `sudo systemctl stop law_bot`
2. Обновите код: `git pull origin main`
3. Обновите зависимости: `pip install -r requirements.txt`
4. Запустите сервис: `sudo systemctl start law_bot`

## Резервное копирование

Регулярно создавайте резервные копии базы данных и папки с загруженными документами:

```bash
# Резервное копирование базы данных
pg_dump -U username -h localhost dbname > backup_$(date +%Y%m%d_%H%M%S).sql

# Резервное копирование загруженных файлов
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/