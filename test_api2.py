#!/usr/bin/env python
import asyncio
import httpx
import json
import sys
sys.path.insert(0, '.')

async def test_api():
    print("Testing API...", flush=True)
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test case questionnaires
            print("Testing /api/requests...", flush=True)
            resp = await client.get('http://localhost:8000/api/requests')
            print(f"Status: {resp.status_code}", flush=True)
            if resp.status_code == 200:
                data = resp.json()
                print(f"Records: {len(data)}", flush=True)
                if data:
                    print(json.dumps(data[0], indent=2, ensure_ascii=False)[:500], flush=True)
            else:
                print(f"Error: {resp.text}", flush=True)
            
            # Test partners
            print("\nTesting /api/partners...", flush=True)
            resp = await client.get('http://localhost:8000/api/partners')
            print(f"Status: {resp.status_code}", flush=True)
            
            # Test users
            print("\nTesting /api/users/list...", flush=True)
            resp = await client.get('http://localhost:8000/api/users/list')
            print(f"Status: {resp.status_code}", flush=True)
            
    except Exception as e:
        print(f"Exception: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api())
