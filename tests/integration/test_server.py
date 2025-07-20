"""
Quick server test to verify FastAPI can start
"""
import sys
sys.path.append('.')

import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_server_basic():
    """Test that server can start and respond to basic requests"""
    # Mock the database initialization to avoid DB dependencies  
    with patch('be.src.main.init_db') as mock_init_db:
        mock_init_db.return_value = asyncio.Future()
        mock_init_db.return_value.set_result(None)
        
        from be.src.main import app
        
        with TestClient(app) as client:
            # Test health endpoint
            response = client.get("/health")
            print(f"Health check: {response.status_code} - {response.json()}")
            assert response.status_code == 200
            
            # Test API status
            response = client.get("/api/status")
            print(f"API status: {response.status_code} - {response.json()}")
            assert response.status_code == 200
            
            print("✅ Server basic functionality tests passed!")

if __name__ == "__main__":
    test_server_basic()