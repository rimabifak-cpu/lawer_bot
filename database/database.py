"""
Модуль подключения к базе данных с оптимизированным пулом соединений
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import asynccontextmanager
from config.settings import settings

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Определяем путь к базе данных
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'law_bot.db')
sqlite_url = f"sqlite+aiosqlite:///{db_path}"

# Используем переменную окружения или SQLite по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL", sqlite_url)

# Для PostgreSQL заменяем postgresql:// на postgresql+asyncpg://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

# Добавляем параметры подключения для PostgreSQL
if "postgresql+asyncpg" in DATABASE_URL:
   pass  # SSL не требуется для localhost

#if "postgresql+asyncpg" in DATABASE_URL:
#    if "?" not in DATABASE_URL:
#        DATABASE_URL += "?ssl=require"
#    else:
#        DATABASE_URL += "&ssl=require"

# Определяем параметры пула в зависимости от типа базы данных
if DATABASE_URL.startswith("sqlite"):
    # Для SQLite используем NullPool или QueuePool с ограниченными настройками
    # SQLite не поддерживает одновременные подключения, поэтому ограничиваем пул
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    logger.info("Создан движок SQLite с QueuePool")
else:
    # Для PostgreSQL и других баз данных используем QueuePool с оптимальными настройками
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800,
        echo=settings.DEBUG
    )
    logger.info("Создан движок базы данных с QueuePool")

# Создаем фабрику сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


@asynccontextmanager
async def get_db():
    """
    Асинхронный контекстный менеджер для получения сессии базы данных.
    
    Использование:
        async with get_db() as db:
            result = await db.execute(query)
    
    Обеспечивает автоматическое закрытие сессии и обработку ошибок.
    """
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Ошибка при работе с базой данных: {e}")
        raise
    finally:
        await session.close()


# Зависимость для FastAPI
async def get_db_session():
    """
    Зависимость для FastAPI для получения сессии базы данных.
    
    Использование в FastAPI:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Ошибка при работе с базой данных: {e}")
        raise
    finally:
        await session.close()


async def init_db():
    """
    Инициализация базы данных - создание всех таблиц
    """
    from database.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("База данных инициализирована")


async def close_db():
    """
    Закрытие соединений с базой данных
    """
    await engine.dispose()
    logger.info("Соединения с базой данных закрыты")
