"""
Миграция: Изменение типа telegram_id с Integer на BigInteger
"""
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from config.settings import settings

async def migrate():
    """Изменяем тип колонки telegram_id на BIGINT"""
    
    # Импортируем engine из database
    from database.database import engine
    
    async with engine.begin() as conn:
        # Для PostgreSQL
        if settings.DATABASE_URL.startswith("postgresql"):
            await conn.execute(text("""
                ALTER TABLE users 
                ALTER COLUMN telegram_id TYPE BIGINT
            """))
            print("✅ Миграция выполнена: telegram_id изменён на BIGINT")
        else:
            print("⚠️ Миграция не требуется для SQLite")

if __name__ == "__main__":
    asyncio.run(migrate())
