import asyncio
import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import engine
from database.models import Base

async def init_tables():
    """Инициализация всех таблиц в базе данных"""
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
    print("Все таблицы успешно созданы в базе данных!")

async def migrate_referral_tables():
    """Миграция для добавления новых таблиц реферальной программы"""
    from sqlalchemy import text
    
    async with engine.begin() as conn:
        # Проверяем, существуют ли уже таблицы
        try:
            # Создаём таблицу partner_revenues
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS partner_revenues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    description TEXT,
                    client_reference VARCHAR(255),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (partner_id) REFERENCES users(id)
                )
            """))
            print("✓ Таблица partner_revenues создана")
        except Exception as e:
            print(f"Таблица partner_revenues уже существует или ошибка: {e}")
        
        try:
            # Создаём таблицу referral_payouts
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS referral_payouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    status VARCHAR(50) DEFAULT 'pending',
                    paid_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referrer_id) REFERENCES users(id)
                )
            """))
            print("✓ Таблица referral_payouts создана")
        except Exception as e:
            print(f"Таблица referral_payouts уже существует или ошибка: {e}")
    
    print("\nМиграция завершена!")

async def main():
    """Главная функция"""
    print("=== Инициализация базы данных ===\n")
    
    # Сначала создаём все таблицы из моделей
    await init_tables()
    
    print("\n=== Миграция реферальной программы ===\n")
    
    # Затем применяем миграции для новых таблиц
    await migrate_referral_tables()

if __name__ == "__main__":
    asyncio.run(main())