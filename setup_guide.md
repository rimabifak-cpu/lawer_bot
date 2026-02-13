# Руководство по настройке и запуску телеграм бота

## Подготовка окружения

### Установка Python

Убедитесь, что у вас установлен Python 3.9 или выше:

```bash
python --version
```

Если Python не установлен, скачайте его с официального сайта: https://www.python.org/downloads/

### Установка PostgreSQL

Для хранения данных используется PostgreSQL. Установите его:

#### Windows:
1. Скачайте PostgreSQL с https://www.postgresql.org/download/windows/
2. Следуйте инструкциям установщика
3. Запомните имя пользователя (по умолчанию postgres) и пароль

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### macOS:
```bash
brew install postgresql
```

## Создание базы данных

1. Запустите PostgreSQL командой:
```bash
sudo -u postgres psql  # Linux/macOS
```
или откройте pgAdmin и подключитесь к серверу.

2. Создайте базу данных:
```sql
CREATE DATABASE law_bot_db;
CREATE USER law_bot_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE law_bot_db TO law_bot_user;
\q
```

## Клонирование репозитория

```bash
git clone <repository-url>
cd law_bot
```

## Установка зависимостей

Создайте виртуальное окружение:

```bash
python -m venv venv
```

Активируйте его:

#### Windows:
```bash
venv\Scripts\activate
```

#### Linux/macOS:
```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=8429912645:AAG95x5WDgqF8r42zFwnF8oLTPSGdQmMcUM
ADMIN_CHAT_ID=your_admin_chat_id
DATABASE_URL=postgresql+asyncpg://law_bot_user:secure_password@localhost/law_bot_db
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=20971520
DEBUG=True
```

## Настройка Telegram бота

1. Найдите в Telegram @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания нового бота
4. Получите токен и добавьте его в переменную `BOT_TOKEN`

## Запуск приложения

### Запуск бота

```bash
python -m bot.main
```

### Запуск админ-панели

В новом терминале (предварительно активировав виртуальное окружение):

```bash
cd admin_panel
uvicorn app:app --reload
```

## Тестирование приложения

Для запуска тестов:

```bash
pytest test_bot.py
```

## Настройка webhook (опционально)

Если вы хотите использовать webhook вместо polling, установите переменную окружения:

```env
USE_WEBHOOK=True
WEBHOOK_URL=https://your-domain.com/webhook
```

## Использование админ-панели

После запуска админ-панели перейдите по адресу http://localhost:8000

На этой странице вы сможете:
- Просматривать все поступающие заявки
- Изменять статусы заявок
- Просматривать базу партнеров
- Отправлять рассылки

## Возможные проблемы и их решение

### Проблема с подключением к базе данных:
- Проверьте, запущен ли PostgreSQL
- Убедитесь, что строка подключения указана правильно
- Проверьте, созданы ли база данных и пользователь

### Бот не отвечает:
- Проверьте, что токен бота указан правильно
- Убедитесь, что бот не заблокирован пользователем
- Проверьте сетевое соединение

### Ошибка при загрузке файлов:
- Проверьте права доступа к папке uploads
- Убедитесь, что размер файла не превышает MAX_FILE_SIZE

## Безопасность

- Не храните токены и пароли в открытом виде в репозитории
- Используйте strong passwords для базы данных
- Регулярно обновляйте зависимости
- В продакшене установите DEBUG=False

## Дополнительные настройки

### Настройка логирования

Для включения детального логирования измените уровень логирования в файле `bot/main.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # для детального логирования
```

### Настройка папки для загрузки файлов

По умолчанию файлы сохраняются в папку `./uploads`, но вы можете изменить это в настройках:

```env
UPLOAD_FOLDER=/path/to/your/upload/folder
```

Убедитесь, что папка существует и доступна для записи.