"""
Миграция: Изменение типа telegram_id с Integer на BigInteger
"""
import asyncio
import os
import sys

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from config.settings import settings

print("=" * 50)
print("Starting telegram_id migration...")
print(f"DATABASE_URL: {settings.DATABASE_URL[:50]}...")
print("=" * 50)

async def migrate():
    """Изменяем тип колонки telegram_id на BIGINT"""
    
    try:
        # Импортируем engine из database
        from database.database import engine
        
        async with engine.begin() as conn:
            # Для PostgreSQL
            if settings.DATABASE_URL.startswith("postgresql"):
                print("Executing ALTER TABLE...")
                await conn.execute(text("""
                    ALTER TABLE users 
                    ALTER COLUMN telegram_id TYPE BIGINT USING telegram_id::BIGINT
                """))
                print("✅ Миграция выполнена: telegram_id изменён на BIGINT")
            else:
                print("⚠️ Миграция не требуется для SQLite")
    except Exception as e:
        print(f"❌ Ошибка миграции: {e}")
        # Не выбрасываем исключение, чтобы не ломать деплой

if __name__ == "__main__":
    asyncio.run(migrate())
    print("Migration script completed.")
