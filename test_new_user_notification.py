import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import get_db
from database.models import User
from config.settings import settings
from bot.main import bot
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def test_new_user_notification():
    """Тест отправки уведомления о новом пользователе"""
    test_user_id = 123456789
    test_username = "testuser"
    test_first_name = "Test"
    test_last_name = "User"
    
    print("Тестирование функции отправки уведомления о новом пользователе...")
    
    async with get_db() as db:
        try:
            # Проверяем, существует ли уже пользователь с таким ID
            result = await db.execute(select(User).filter(User.telegram_id == test_user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                user = User(
                    telegram_id=test_user_id,
                    username=test_username,
                    first_name=test_first_name,
                    last_name=test_last_name
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
                print(f"Создан тестовый пользователь: {test_user_id}")
            
            # Импортируем и вызываем функцию отправки уведомления
            from bot.handlers.start import send_new_user_notification
            await send_new_user_notification(user)
            
            print("Уведомление отправлено")
            return True
            
        except Exception as e:
            print(f"Ошибка: {e}")
            await db.rollback()
            return False

async def cleanup():
    """Удаление тестового пользователя"""
    test_user_id = 123456789
    
    async with get_db() as db:
        try:
            result = await db.execute(select(User).filter(User.telegram_id == test_user_id))
            user = result.scalar_one_or_none()
            
            if user:
                await db.delete(user)
                await db.commit()
                print(f"Удален тестовый пользователь: {test_user_id}")
            
        except Exception as e:
            print(f"Ошибка при удалении тестового пользователя: {e}")
            await db.rollback()

if __name__ == "__main__":
    try:
        # Запускаем тест
        asyncio.run(test_new_user_notification())
        
    finally:
        # Удаляем тестового пользователя
        asyncio.run(cleanup())