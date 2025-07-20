"""
Tests for WebSocket connection management
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
import json

import sys
sys.path.append('.')
sys.path.append('..')

from be.src.websocket_manager import WebSocketManager


@pytest.fixture
def websocket_manager():
    """WebSocket manager instance for testing"""
    return WebSocketManager()


@pytest.fixture
def mock_websocket():
    """Mock WebSocket connection"""
    websocket = MagicMock()
    websocket.accept = AsyncMock()
    websocket.send_text = AsyncMock()
    return websocket


@pytest.mark.asyncio
async def test_connect_websocket(websocket_manager, mock_websocket):
    """Test WebSocket connection"""
    conversation_id = "test-conversation"
    
    await websocket_manager.connect(mock_websocket, conversation_id)
    
    # Verify connection was accepted
    mock_websocket.accept.assert_called_once()
    
    # Verify connection was added to active connections
    assert conversation_id in websocket_manager.active_connections
    assert mock_websocket in websocket_manager.active_connections[conversation_id]
    assert websocket_manager.get_connection_count(conversation_id) == 1


def test_disconnect_websocket(websocket_manager, mock_websocket):
    """Test WebSocket disconnection"""
    conversation_id = "test-conversation"
    
    # Manually add connection (simulating previous connect)
    websocket_manager.active_connections[conversation_id] = [mock_websocket]
    
    websocket_manager.disconnect(mock_websocket, conversation_id)
    
    # Verify connection was removed
    assert conversation_id not in websocket_manager.active_connections


@pytest.mark.asyncio
async def test_send_personal_message(websocket_manager, mock_websocket):
    """Test sending personal message"""
    message = {"type": "test", "data": "hello"}
    
    await websocket_manager.send_personal_message(message, mock_websocket)
    
    # Verify message was sent as JSON
    mock_websocket.send_text.assert_called_once_with(json.dumps(message))


@pytest.mark.asyncio
async def test_broadcast_to_conversation(websocket_manager, mock_websocket):
    """Test broadcasting to conversation"""
    conversation_id = "test-conversation"
    message = {"type": "broadcast", "data": "hello all"}
    
    # Add connection
    websocket_manager.active_connections[conversation_id] = [mock_websocket]
    
    await websocket_manager.broadcast_to_conversation(message, conversation_id)
    
    # Verify message was sent to all connections in conversation
    mock_websocket.send_text.assert_called_once_with(json.dumps(message))


@pytest.mark.asyncio
async def test_broadcast_to_nonexistent_conversation(websocket_manager):
    """Test broadcasting to conversation with no active connections"""
    message = {"type": "broadcast", "data": "hello"}
    
    # Should not raise error
    await websocket_manager.broadcast_to_conversation(message, "nonexistent")


def test_get_connection_count(websocket_manager, mock_websocket):
    """Test connection count methods"""
    conversation_id = "test-conversation"
    
    # Initially no connections
    assert websocket_manager.get_connection_count() == 0
    assert websocket_manager.get_connection_count(conversation_id) == 0
    
    # Add connection
    websocket_manager.active_connections[conversation_id] = [mock_websocket]
    
    # Verify counts
    assert websocket_manager.get_connection_count() == 1
    assert websocket_manager.get_connection_count(conversation_id) == 1


def test_get_active_conversations(websocket_manager, mock_websocket):
    """Test getting active conversation list"""
    # Initially no conversations
    assert websocket_manager.get_active_conversations() == []
    
    # Add conversations
    websocket_manager.active_connections["conv1"] = [mock_websocket]
    websocket_manager.active_connections["conv2"] = [mock_websocket]
    
    active_conversations = websocket_manager.get_active_conversations()
    assert len(active_conversations) == 2
    assert "conv1" in active_conversations
    assert "conv2" in active_conversations


@pytest.mark.asyncio
async def test_multiple_connections_same_conversation(websocket_manager):
    """Test multiple WebSocket connections for same conversation"""
    conversation_id = "test-conversation"
    ws1 = MagicMock()
    ws1.accept = AsyncMock()
    ws2 = MagicMock()
    ws2.accept = AsyncMock()
    
    # Connect both WebSockets
    await websocket_manager.connect(ws1, conversation_id)
    await websocket_manager.connect(ws2, conversation_id)
    
    # Verify both connections are tracked
    assert websocket_manager.get_connection_count(conversation_id) == 2
    assert ws1 in websocket_manager.active_connections[conversation_id]
    assert ws2 in websocket_manager.active_connections[conversation_id]