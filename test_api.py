import httpx
import asyncio
import traceback

async def test_api():
    try:
        # Test the stats endpoint
        async with httpx.AsyncClient() as client:
            print("Testing /api/stats...")
            response = await client.get("http://127.0.0.1:8000/api/stats")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
            print("\nTesting /api/users...")
            response2 = await client.get("http://127.0.0.1:8000/api/users")
            print(f"Status: {response2.status_code}")
            print(f"Response: {response2.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

asyncio.run(test_api())
