"""
Debug Jina API call format
"""
import asyncio
import httpx
import json

async def debug_jina_api():
    """Debug the exact API format needed for Jina"""
    
    # Check what we're sending
    api_key = "jina_725b97a3142644f88ca2d991f5804685iSODX4GGe9GindaMJbYPPFDLhLlf"
    
    client = httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        timeout=30.0
    )
    
    # Try basic embedding call based on Jina docs
    payload = {
        "model": "jina-embeddings-v2-base-en",
        "input": ["test text for embeddings"]
    }
    
    print("🔍 Debugging Jina API call...")
    print(f"📤 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = await client.post(
            "https://api.jina.ai/v1/embeddings",
            json=payload
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 400:
            print(f"❌ Error response: {response.text}")
        else:
            result = response.json()
            print(f"✅ Success: {len(result.get('data', []))} embeddings")
            
    except Exception as e:
        print(f"💥 Exception: {e}")
    
    await client.aclose()

if __name__ == "__main__":
    asyncio.run(debug_jina_api())