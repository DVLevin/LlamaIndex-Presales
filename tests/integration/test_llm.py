"""
Test script for OpenRouter LLM integration
"""
import asyncio
import sys
sys.path.append('.')
sys.path.append('..')

from ai.src.llm_integration import test_llm_integration, get_openrouter_client
from ai.src.config import get_ai_settings


async def test_basic_llm():
    """Test basic LLM functionality"""
    print("🧪 Testing OpenRouter LLM Integration...")
    
    # Test configuration
    settings = get_ai_settings()
    print(f"✅ Configuration loaded: {settings.default_llm_model}")
    print(f"✅ API Key configured: {settings.openrouter_api_key[:10]}...")
    
    # Test LLM integration
    try:
        result = await test_llm_integration()
        
        if result["status"] == "success":
            print("✅ LLM Integration Test PASSED")
            print(f"📤 LLM Response: {result['llm_response'][:100]}...")
            print(f"🤖 Agent Response: {result['agent_response'][:100]}...")
            print(f"🎯 Model: {result['model']}")
        else:
            print("❌ LLM Integration Test FAILED")
            print(f"💥 Error: {result['error']}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
    
    print("\n🎉 OpenRouter LLM integration test complete!")


if __name__ == "__main__":
    asyncio.run(test_basic_llm())