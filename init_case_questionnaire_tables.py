"""
Script for creating case questionnaire tables in database
Run: python -c "import asyncio; from init_case_questionnaire_tables import migrate_case_tables; asyncio.run(migrate_case_tables())"
"""
import asyncio
import sys
import os

# Add path to project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import engine
from sqlalchemy import text


async def migrate_case_questionnaire_tables():
    """Migration for adding case questionnaire tables"""
    
    async with engine.begin() as conn:
        # Create case_questionnaires table
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS case_questionnaires (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    parties_info TEXT,
                    dispute_subject TEXT,
                    legal_basis TEXT,
                    chronology TEXT,
                    evidence TEXT,
                    procedural_history TEXT,
                    client_goal TEXT,
                    status VARCHAR(50) DEFAULT 'sent',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            print("[OK] Table case_questionnaires created")
        except Exception as e:
            print(f"[ERROR] Table case_questionnaires: {e}")
        
        # Create case_questionnaire_documents table
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS case_questionnaire_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    questionnaire_id INTEGER NOT NULL,
                    section VARCHAR(50),
                    file_path VARCHAR(500),
                    file_type VARCHAR(50),
                    original_name VARCHAR(255),
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (questionnaire_id) REFERENCES case_questionnaires(id)
                )
            """))
            print("[OK] Table case_questionnaire_documents created")
        except Exception as e:
            print(f"[ERROR] Table case_questionnaire_documents: {e}")
    
    print("\n[SUCCESS] Case questionnaire tables migration completed!")


async def main():
    """Main function"""
    print("=== Case Questionnaire Tables Migration ===\n")
    await migrate_case_questionnaire_tables()


if __name__ == "__main__":
    asyncio.run(main())
