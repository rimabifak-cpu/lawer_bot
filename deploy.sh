#!/bin/bash
# Скрипт для первичного деплоя на сервере
# Запускать на Oracle Cloud сервере

set -e

echo "🚀 Law Bot - Первичный деплой на сервер"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker не найден. Установка...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo -e "${GREEN}Docker установлен!${NC}"
fi

# Проверка наличия Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose не найден. Установка...${NC}"
    sudo apt-get update
    sudo apt-get install -y docker-compose
    echo -e "${GREEN}Docker Compose установлен!${NC}"
fi

# Создание директории для проекта
PROJECT_DIR=~/law_bot
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}Создание директории проекта...${NC}"
    mkdir -p $PROJECT_DIR
fi

cd $PROJECT_DIR

# Клонирование репозитория (если ещё не склонирован)
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Введите URL вашего GitHub репозитория:${NC}"
    read -p "GitHub Repo URL: " REPO_URL
    git clone $REPO_URL .
fi

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Создание .env файла...${NC}"
    cp .env.docker .env
    echo -e "${RED}⚠️  ВАЖНО: Отредактируйте .env файл и укажите ваши данные!${NC}"
    echo -e "${YELLOW}Для редактирования выполните: nano .env${NC}"
    echo -e "${YELLOW}После редактирования запустите скрипт снова:${NC}"
    echo -e "${GREEN}   bash deploy.sh${NC}"
    exit 1
fi

# Создание директорий для данных
mkdir -p uploads logs

# Остановка старых контейнеров (если есть)
echo -e "${YELLOW}Остановка старых контейнеров...${NC}"
docker-compose down || true

# Сборка и запуск контейнеров
echo -e "${GREEN}🔨 Сборка контейнеров...${NC}"
docker-compose build

echo -e "${GREEN}🚀 Запуск контейнеров...${NC}"
docker-compose up -d

# Инициализация базы данных
echo -e "${YELLOW}Инициализация базы данных...${NC}"
sleep 10
docker-compose exec -T bot python init_db.py || echo "⚠️  Инициализация БД завершена с предупреждениями"

# Вывод статуса
echo ""
echo -e "${GREEN}✅ Деплой завершён!${NC}"
echo ""
echo "📊 Статус сервисов:"
docker-compose ps
echo ""
echo "🔗 Админ-панель: http://$(curl -s ifconfig.me):8000"
echo ""
echo "📋 Полезные команды:"
echo "   docker-compose logs -f        # Логи всех сервисов"
echo "   docker-compose logs bot       # Логи бота"
echo "   docker-compose logs admin     # Логи админки"
echo "   docker-compose restart        # Перезапуск"
echo "   docker-compose down           # Остановка"
echo ""
