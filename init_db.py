"""
Скрипт для инициализации базы данных
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database.models import Base
from config.settings import settings

async def init_db():
    # Создаем engine для подключения к базе данных
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
    
    print("База данных успешно инициализирована!")

if __name__ == "__main__":
    asyncio.run(init_db())