import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_db
from sqlalchemy import text

async def test():
    try:
        print("Starting test...")
        async with get_db() as db:
            print("Got DB session")
            result = await db.execute(text('SELECT COUNT(*) FROM users'))
            count = result.scalar()
            print(f"Users count: {count}")
            print("Database connection OK!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
