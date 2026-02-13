#!/usr/bin/env python
import asyncio
import sys
sys.path.insert(0, '.')

from database.database import get_db
from sqlalchemy import text

async def test_db():
    print("Testing database connection...")
    try:
        async with get_db() as db:
            # Test users table
            result = await db.execute(text('SELECT COUNT(*) FROM users'))
            count = result.fetchone()[0]
            print(f'Users: {count}')
            
            # Test case_questionnaires table
            result = await db.execute(text('SELECT COUNT(*) FROM case_questionnaires'))
            count = result.fetchone()[0]
            print(f'Case questionnaires: {count}')
            
            # Test partner_profiles table
            result = await db.execute(text('SELECT COUNT(*) FROM partner_profiles'))
            count = result.fetchone()[0]
            print(f'Partner profiles: {count}')
            
            # Test referral_relationships table
            result = await db.execute(text('SELECT COUNT(*) FROM referral_relationships'))
            count = result.fetchone()[0]
            print(f'Referral relationships: {count}')
            
            print("\nDatabase OK!")
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_db())
