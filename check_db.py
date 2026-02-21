#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from database.database import get_db
from sqlalchemy import text
import asyncio

async def check_bot():
    try:
        async with get_db() as db:
            # Проверка количества пользователей
            result = await db.execute(text('SELECT COUNT(*) FROM users'))
            count = result.fetchone()[0]
            print(f'Пользователей в базе: {count}')
            
            # Проверка количества партнёров
            result = await db.execute(text('SELECT COUNT(*) FROM partner_profiles'))
            count = result.fetchone()[0]
            print(f'Партнёров в базе: {count}')
            
            # Проверка количества реферальных связей
            result = await db.execute(text('SELECT COUNT(*) FROM referral_relationships'))
            count = result.fetchone()[0]
            print(f'Реферальных связей: {count}')
            
            # Проверка количества анкет
            result = await db.execute(text('SELECT COUNT(*) FROM case_questionnaires'))
            count = result.fetchone()[0]
            print(f'Анкет дел: {count}')
    except Exception as e:
        print(f'Ошибка: {e}')

asyncio.run(check_bot())