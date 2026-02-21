#!/usr/bin/env python3
import sys
import os
import traceback
import logging
sys.path.append('.')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.debug("Importing database modules...")
    from database.database import get_db
    from database.models import User
    import asyncio
    logger.debug("Database modules imported successfully")
    
    async def test_db():
        logger.debug("Getting database session...")
        try:
            async with get_db() as db:
                logger.debug("Session obtained")
                result = await db.execute(User.__table__.select())
                users = result.scalars().all()
                logger.debug(f"Users in DB: {len(users)}")
                for user in users:
                    logger.debug(f"  - {user.telegram_id}")
                return users
        except Exception as e:
            logger.error(f"Database session error: {e}")
            logger.error(traceback.format_exc())
            raise
            
    logger.debug("Running async test...")
    users = asyncio.run(test_db())
    logger.info("Database test passed")
    logger.info(f"Found {len(users)} users")
    
except Exception as e:
    logger.error(f'ERROR: {type(e).__name__}: {e}')
    logger.error(traceback.format_exc())
