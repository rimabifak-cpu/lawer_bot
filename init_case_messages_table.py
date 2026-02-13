"""
Script for creating case messages table in database
Run: python -c "import asyncio; from init_case_messages_table import migrate_messages; asyncio.run(migrate_messages())"
"""
import asyncio
import sys
import os

# Add path to project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import engine
from sqlalchemy import text


async def migrate_case_messages_table():
    """Migration for adding case messages table"""
    
    async with engine.begin() as conn:
        # Create case_messages table
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS case_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    questionnaire_id INTEGER NOT NULL,
                    sender_id INTEGER NOT NULL,
                    sender_type VARCHAR(20) NOT NULL,
                    message_content TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (questionnaire_id) REFERENCES case_questionnaires(id),
                    FOREIGN KEY (sender_id) REFERENCES users(id)
                )
            """))
            print("[OK] Table case_messages created")
        except Exception as e:
            print(f"[ERROR] Table case_messages: {e}")
        
        # Create index for faster queries
        try:
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_case_messages_questionnaire 
                ON case_messages(questionnaire_id)
            """))
            print("[OK] Index created")
        except Exception as e:
            print(f"[ERROR] Index: {e}")
    
    print("\n[SUCCESS] Case messages table migration completed!")


async def main():
    """Main function"""
    print("=== Case Messages Table Migration ===\n")
    await migrate_case_messages_table()


if __name__ == "__main__":
    asyncio.run(main())
