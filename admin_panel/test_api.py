import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import AsyncSessionLocal
from database.models import User, PartnerProfile, CaseQuestionnaire, ReferralRelationship

async def test_data():
    print("Testing database connection...")
    
    async with AsyncSessionLocal() as session:
        # Test users
        result = await session.execute("SELECT COUNT(*) FROM users")
        count = result.fetchone()[0]
        print(f"Users: {count}")
        
        # Test partners
        result = await session.execute("SELECT COUNT(*) FROM partner_profiles")
        count = result.fetchone()[0]
        print(f"Partner Profiles: {count}")
        
        # Test case questionnaires
        result = await session.execute("SELECT COUNT(*) FROM case_questionnaires")
        count = result.fetchone()[0]
        print(f"Case Questionnaires: {count}")
        
        # Test referral relationships
        result = await session.execute("SELECT COUNT(*) FROM referral_relationships")
        count = result.fetchone()[0]
        print(f"Referral Relationships: {count}")
        
        print("\nAll tests passed!")

if __name__ == "__main__":
    asyncio.run(test_data())
