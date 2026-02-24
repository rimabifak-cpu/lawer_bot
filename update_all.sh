#!/bin/bash

echo "=========================================="
echo "  Law Bot - Обновление всех проектов"
echo "=========================================="

# Список проектов
PROJECTS=(
    "/opt/law_bot"
    "/opt/project2"
    "/opt/project3"
)

for PROJECT in "${PROJECTS[@]}"; do
    if [ -d "$PROJECT" ]; then
        echo ""
        echo "=========================================="
        echo "  Обновление: $PROJECT"
        echo "=========================================="
        
        cd "$PROJECT"
        
        # Git pull
        echo "[1/3] Получение обновлений..."
        git pull origin main
        
        if [ $? -ne 0 ]; then
            echo "❌ Ошибка git pull в $PROJECT"
            continue
        fi
        
        # Build
        echo "[2/3] Пересборка..."
        docker-compose build --no-cache
        
        # Restart
        echo "[3/3] Перезапуск..."
        docker-compose up -d --force-recreate
        
        echo "✅ $PROJECT обновлён"
    else
        echo "⚠️ $PROJECT не существует, пропускаем"
    fi
done

echo ""
echo "=========================================="
echo "  Все проекты обновлены!"
echo "=========================================="
echo ""
echo "Статус всех контейнеров:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
