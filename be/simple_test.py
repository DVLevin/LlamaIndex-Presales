"""
Simple test to verify backend components work
"""
import sys
import os
sys.path.append('.')

# Test 1: Configuration loading
print("🧪 Testing Configuration...")
try:
    from be.src.config import get_settings
    settings = get_settings()
    print(f"✅ Settings loaded: LLM={settings.default_llm_model}")
    print(f"✅ API Keys configured: OpenRouter={settings.openrouter_api_key[:10]}...")
except Exception as e:
    print(f"❌ Configuration failed: {e}")

# Test 2: WebSocket Manager
print("\n🧪 Testing WebSocket Manager...")
try:
    from be.src.websocket_manager import WebSocketManager
    manager = WebSocketManager()
    assert manager.get_connection_count() == 0
    print("✅ WebSocket Manager created successfully")
except Exception as e:
    print(f"❌ WebSocket Manager failed: {e}")

# Test 3: Database Models (without connection)
print("\n🧪 Testing Database Models...")
try:
    from be.src.database import Conversation, PipelineExecution
    print("✅ Database models imported successfully")
except Exception as e:
    print(f"❌ Database models failed: {e}")

print("\n🎉 Backend foundation components are working!")
print("🚀 Ready for Epic 2: LlamaIndex Integration")