#!/bin/bash

echo "=========================================="
echo "  Law Bot - Автоматическая установка"
echo "=========================================="

# Обновление системы
echo "[1/8] Обновление системы..."
apt update && apt upgrade -y

# Установка Docker
echo "[2/8] Установка Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Установка Docker Compose
echo "[3/8] Установка Docker Compose..."
apt install -y docker-compose

# Установка Git
echo "[4/8] Установка Git..."
apt install -y git

# Клонируем репозиторий (если ещё не склонирован)
echo "[5/8] Загрузка кода бота..."
if [ ! -d "/opt/law_bot" ]; then
    git clone https://github.com/rimabifak-cpu/lawer_bot.git /opt/law_bot
fi
cd /opt/law_bot

# Создаём .env файл
echo "[6/8] Настройка переменных окружения..."
cat > .env << 'EOF'
BOT_TOKEN=8429912645:AAG95x5WDgqF8r42zFwnF8oLTPSGdQmMcUM
ADMIN_CHAT_ID=-1003899118823
DATABASE_URL=postgresql://law_bot_user:LawBot2024Secure!@localhost:5432/law_bot_db
UPLOAD_FOLDER=/opt/law_bot/uploads
MAX_FILE_SIZE=20971520
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png,doc,docx
DEBUG=False
EOF

# Создаём docker-compose.yml
echo "[7/8] Создание docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: law_bot_db
    environment:
      POSTGRES_DB: law_bot_db
      POSTGRES_USER: law_bot_user
      POSTGRES_PASSWORD: LawBot2024Secure!
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - law_bot_network
    restart: unless-stopped

  bot:
    build: .
    container_name: law_bot
    env_file: .env
    depends_on:
      - db
    volumes:
      - ./uploads:/opt/law_bot/uploads
    networks:
      - law_bot_network
    restart: unless-stopped

  admin:
    build:
      context: .
      dockerfile: Dockerfile.admin
    container_name: law_bot_admin
    env_file: .env
    depends_on:
      - db
    ports:
      - "8000:8000"
    networks:
      - law_bot_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  law_bot_network:
    driver: bridge
EOF

# Запускаем бота
echo "[8/8] Запуск бота..."
docker-compose up -d --build

# Ждём запуска
sleep 10

# Показываем логи
echo ""
echo "=========================================="
echo "  Установка завершена!"
echo "=========================================="
echo ""
echo "Статус сервисов:"
docker-compose ps
echo ""
echo "Логи бота (последние 20 строк):"
docker-compose logs --tail=20 bot
echo ""
echo "=========================================="
echo "  Админка: http://$(curl -s ifconfig.me):8000"
echo "=========================================="
