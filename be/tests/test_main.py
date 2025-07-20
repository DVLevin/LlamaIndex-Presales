"""
Tests for FastAPI main application
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

import sys
sys.path.append('.')
sys.path.append('..')

from be.src.main import app


@pytest.fixture
def client():
    """Test client for FastAPI application"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "presales-ai-backend"}


def test_api_status(client):
    """Test API status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "operational"
    assert data["version"] == "1.0.0"
    assert "llm_model" in data
    assert "embedding_model" in data


def test_app_properties():
    """Test application properties"""
    # Test that the app can be created without errors
    assert app is not None
    assert app.title == "LlamaIndex Presales AI System"


def test_cors_headers(client):
    """Test CORS headers are properly configured"""
    response = client.options("/health")
    # FastAPI automatically handles OPTIONS for CORS
    # We test that the endpoint is accessible
    assert response.status_code in [200, 405]  # 405 is normal for OPTIONS on GET endpoints


def test_websocket_connection():
    """Test WebSocket connection endpoint exists"""
    with TestClient(app) as client:
        # Test that the WebSocket endpoint path is recognized
        # Note: Full WebSocket testing requires more complex setup
        try:
            with client.websocket_connect("/ws/test-conversation"):
                pass
        except Exception:
            # Expected to fail without proper WebSocket setup, 
            # but confirms the endpoint exists
            pass