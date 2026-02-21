# Деплой юридического Telegram бота на Oracle Cloud Free

## 📋 Оглавление

1. [Создание сервера Oracle Cloud](#1-создание-сервера-oracle-cloud)
2. [Подключение к серверу](#2-подключение-к-серверу)
3. [Настройка брандмауэра Oracle](#3-настройка-брандмауэра-oracle)
4. [Установка ПО на сервер](#4-установка-по-на-сервер)
5. [Настройка PostgreSQL](#5-настройка-postgresql)
6. [Загрузка проекта](#6-загрузка-проекта)
7. [Настройка окружения](#7-настройка-окружения)
8. [Запуск бота и админки](#8-запуск-бота-и-админки)
9. [Настройка автозапуска (systemd)](#9-настройка-автозапуска-systemd)
10. [Настройка домена и HTTPS](#10-настройка-домена-и-https)

---

## 1. Создание сервера Oracle Cloud

### Шаг 1.1: Регистрация и вход
1. Перейдите на [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
2. Зарегистрируйтесь или войдите в аккаунт

### Шаг 1.2: Создание инстанса
1. В консоли перейдите: **Compute** → **Instances**
2. Нажмите **Create Instance**
3. Выберите:
   - **Compartment**: ваше основное compartment
   - **Instance name**: `law-bot-server`
   - **Image**: Ubuntu 22.04 или 24.04
   - **Shape**: `VM.Standard.A1.Flex` (бесплатный ARM)
     - OCPUs: 2
     - Memory: 12 GB
   - **Networking**: 
     - Выберите VCN (создастся автоматически)
     - Assign public IPv4 address: ✅
   - **SSH keys**: 
     - Выберите "Upload public key files"
     - Загрузите ваш публичный ключ (`~/.ssh/id_rsa.pub` или создайте новый)

4. Нажмите **Create**

### Шаг 1.3: Запишите данные
После создания запишите:
- **Public IP адрес** сервера
- **Имя пользователя** (обычно `ubuntu` для Ubuntu)

---

## 2. Подключение к серверу

### Вариант A: Через SSH (рекомендуется)

```bash
# Подключение с использованием приватного ключа
ssh -i /path/to/private_key ubuntu@<PUBLIC_IP>

# Пример для Windows (PowerShell)
ssh -i C:\Users\HONOR\.ssh\id_rsa ubuntu@<PUBLIC_IP>
```

### Вариант B: Через Cloud Shell
1. В консоли Oracle нажмите **Cloud Shell** (иконка терминала вверху)
2. Подключитесь: `ssh -i ~/.ssh/id_rsa ubuntu@<PUBLIC_IP>`

### Первая настройка сервера

```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade -y

# Установка базовых утилит
sudo apt install -y git curl wget nano htop net-tools

# Настройка часового пояса
sudo timedatectl set-timezone Europe/Moscow
```

---

## 3. Настройка брандмауэра Oracle

### Шаг 3.1: Брандмауэр в Oracle Console
1. В консоли перейдите: **Networking** → **Virtual Cloud Networks**
2. Выберите вашу VCN
3. Кликните на **Security Lists** → **Default Security List**
4. Нажмите **Add Ingress Rules**:

| Source CIDR | IP Protocol | Destination Port Range | Description |
|-------------|-------------|------------------------|-------------|
| 0.0.0.0/0   | TCP         | 22                     | SSH         |
| 0.0.0.0/0   | TCP         | 8000                   | Admin Panel |
| 0.0.0.0/0   | TCP         | 80                     | HTTP        |
| 0.0.0.0/0   | TCP         | 443                    | HTTPS       |

### Шаг 3.2: Брандмауэр на сервере (UFW)

```bash
# Включение UFW
sudo ufw enable

# Разрешение портов
sudo ufw allow 22/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Проверка статуса
sudo ufw status
```

---

## 4. Установка ПО на сервер

### Шаг 4.1: Установка Python 3.10+

```bash
# Установка Python и зависимостей
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Проверка версии
python3 --version  # Должна быть 3.10+
```

### Шаг 4.2: Установка PostgreSQL

```bash
# Установка PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Проверка статуса
sudo systemctl status postgresql
```

### Шаг 4.3: Установка дополнительных зависимостей

```bash
# Для работы с PostgreSQL и компиляции пакетов
sudo apt install -y libpq-dev gcc g++ make

# Для работы с файлами
sudo apt install -y libmagic1
```

---

## 5. Настройка PostgreSQL

### Шаг 5.1: Создание пользователя и базы данных

```bash
# Вход в PostgreSQL от имени пользователя postgres
sudo -i -u postgres
psql
```

```sql
-- Создание базы данных
CREATE DATABASE law_bot_db;

-- Создание пользователя
CREATE USER law_bot_user WITH PASSWORD 'your_secure_password_here';

-- Предоставление прав
GRANT ALL PRIVILEGES ON DATABASE law_bot_db TO law_bot_user;

-- Выход из psql
\q

-- Выход из пользователя postgres
exit
```

### Шаг 5.2: Проверка подключения

```bash
# Проверка подключения
psql -U law_bot_user -d law_bot_db -h localhost -W
```

---

## 6. Загрузка проекта

### Вариант A: Через Git (рекомендуется)

```bash
# Создание директории для проекта
mkdir -p ~/law_bot
cd ~/law_bot

# Клонирование репозитория
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ> .

# Или скопируйте файлы через SCP/SFTP
# Из локальной терминала (Windows):
# scp -i C:\Users\HONOR\.ssh\id_rsa -r C:\Users\HONOR\Documents\law_bot\* ubuntu@<PUBLIC_IP>:~/law_bot/
```

### Вариант B: Через SCP

```bash
# С локальной машины (Windows PowerShell)
scp -i C:\Users\HONOR\.ssh\id_rsa -r C:\Users\HONOR\Documents\law_bot\* ubuntu@<PUBLIC_IP>:~/law_bot/
```

---

## 7. Настройка окружения

### Шаг 7.1: Создание виртуального окружения

```bash
cd ~/law_bot

# Создание виртуального окружения
python3 -m venv venv

# Активация
source venv/bin/activate

# Обновление pip
pip install --upgrade pip
```

### Шаг 7.2: Установка зависимостей

```bash
# Установка зависимостей из requirements.txt
pip install -r requirements.txt
```

### Шаг 7.3: Настройка .env файла

```bash
# Копирование примера
cp .env.example .env

# Редактирование
nano .env
```

**Содержимое .env:**

```env
# Токен Telegram бота (получается у @BotFather)
BOT_TOKEN=8429912645:AAG95x5WDgqF8r42zFwnF8oLTPSGdQmMcUM

# ID чата администратора (получить через @userinfobot)
ADMIN_CHAT_ID=ваш_admin_chat_id

# Строка подключения к базе данных
DATABASE_URL=postgresql+asyncpg://law_bot_user:your_secure_password_here@localhost/law_bot_db

# Папка для загрузки файлов
UPLOAD_FOLDER=/home/ubuntu/law_bot/uploads

# Максимальный размер файла в байтах (20MB)
MAX_FILE_SIZE=20971520

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png,doc,docx

# Режим отладки (False для продакшена)
DEBUG=False

# URL message_server (если используется)
MESSAGE_SERVER_URL=http://127.0.0.1:8002

# Хост для админ-панели
ADMIN_HOST=0.0.0.0
ADMIN_PORT=8000
```

### Шаг 7.4: Инициализация базы данных

```bash
# Запуск миграций/инициализации
python init_db.py
```

---

## 8. Запуск бота и админки

### Шаг 8.1: Тестовый запуск

```bash
# Активация виртуального окружения
source venv/bin/activate

# Запуск бота (в одном терминале)
python run_bot.py

# Запуск админ-панели (в другом терминале)
cd admin_panel
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Шаг 8.2: Проверка работы

1. **Бот**: Отправьте `/start` в Telegram
2. **Админка**: Откройте `http://<PUBLIC_IP>:8000`

---

## 9. Настройка автозапуска (systemd)

### Шаг 9.1: Создание сервиса для бота

```bash
sudo nano /etc/systemd/system/law-bot.service
```

**Содержимое `/etc/systemd/system/law-bot.service`:**

```ini
[Unit]
Description=Law Bot Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/law_bot
Environment="PATH=/home/ubuntu/law_bot/venv/bin"
ExecStart=/home/ubuntu/law_bot/venv/bin/python /home/ubuntu/law_bot/run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Шаг 9.2: Создание сервиса для админ-панели

```bash
sudo nano /etc/systemd/system/law-bot-admin.service
```

**Содержимое `/etc/systemd/system/law-bot-admin.service`:**

```ini
[Unit]
Description=Law Bot Admin Panel
After=network.target postgresql.service law-bot.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/law_bot
Environment="PATH=/home/ubuntu/law_bot/venv/bin"
Environment="ADMIN_HOST=0.0.0.0"
Environment="ADMIN_PORT=8000"
ExecStart=/home/ubuntu/law_bot/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Шаг 9.3: Включение и запуск сервисов

```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение сервисов
sudo systemctl enable law-bot
sudo systemctl enable law-bot-admin

# Запуск сервисов
sudo systemctl start law-bot
sudo systemctl start law-bot-admin

# Проверка статуса
sudo systemctl status law-bot
sudo systemctl status law-bot-admin

# Просмотр логов
sudo journalctl -u law-bot -f
sudo journalctl -u law-bot-admin -f
```

### Шаг 9.4: Управление сервисами

```bash
# Перезапуск
sudo systemctl restart law-bot
sudo systemctl restart law-bot-admin

# Остановка
sudo systemctl stop law-bot
sudo systemctl stop law-bot-admin

# Логи
sudo journalctl -u law-bot --since today
sudo journalctl -u law-bot-admin --since today
```

---

## 10. Настройка домена и HTTPS (опционально)

### Шаг 10.1: Покупка домена
Купите домен у любого регистратора (Namecheap, GoDaddy, Reg.ru)

### Шаг 10.2: Настройка DNS
Создайте A-запись:
- **Host**: `@` или `law-bot.yourdomain.com`
- **Value**: `<PUBLIC_IP>`
- **TTL**: Auto

### Шаг 10.3: Установка Nginx

```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Шаг 10.4: Конфигурация Nginx

```bash
sudo nano /etc/nginx/sites-available/law-bot
```

**Содержимое:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Включение сайта
sudo ln -s /etc/nginx/sites-available/law-bot /etc/nginx/sites-enabled/

# Проверка конфигурации
sudo nginx -t

# Перезагрузка Nginx
sudo systemctl restart nginx
```

### Шаг 10.5: Установка SSL сертификата (Let's Encrypt)

```bash
# Установка Certbot
sudo apt install -y certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d your-domain.com

# Автоматическое продление
sudo certbot renew --dry-run
```

---

## 🔧 Диагностика проблем

### Бот не запускается

```bash
# Проверка логов
sudo journalctl -u law-bot -n 50

# Проверка .env
cat /home/ubuntu/law_bot/.env

# Проверка подключения к БД
source venv/bin/activate
python -c "from database.database import get_db; import asyncio; asyncio.run(get_db().__anext__())"
```

### Админка недоступна

```bash
# Проверка порта
sudo netstat -tlnp | grep 8000

# Проверка брандмауэра
sudo ufw status

# Проверка логов
sudo journalctl -u law-bot-admin -n 50
```

### Ошибки PostgreSQL

```bash
# Проверка статуса
sudo systemctl status postgresql

# Проверка логов
sudo tail -f /var/log/postgresql/postgresql-*.log

# Проверка подключения
psql -U law_bot_user -d law_bot_db -h localhost -W
```

---

## 📊 Мониторинг

### Использование ресурсов

```bash
# Использование CPU и памяти
htop

# Использование диска
df -h

# Использование памяти
free -h
```

### Логи приложения

```bash
# Логи бота
tail -f /var/log/syslog | grep law-bot

# Логи админки
tail -f /var/log/syslog | grep law-bot-admin
```

---

## 🚀 Быстрые команды

```bash
# Перезапуск всего
sudo systemctl restart law-bot && sudo systemctl restart law-bot-admin

# Проверка статуса
sudo systemctl status law-bot law-bot-admin

# Обновление кода
cd ~/law_bot && git pull && sudo systemctl restart law-bot law-bot-admin

# Резервное копирование БД
pg_dump -U law_bot_user law_bot_db > backup_$(date +%Y%m%d).sql
```

---

## 📞 Полезные ссылки

- [Oracle Cloud Documentation](https://docs.oracle.com/en-us/iaas/)
- [aiogram Documentation](https://docs.aiogram.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
