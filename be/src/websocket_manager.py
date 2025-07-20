"""
WebSocket connection management for real-time pipeline updates
"""
from typing import Dict, List
from fastapi import WebSocket
import structlog
import json

logger = structlog.get_logger()


class WebSocketManager:
    """Manages WebSocket connections for real-time communication"""
    
    def __init__(self):
        # Map conversation_id -> list of websocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, conversation_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []
        
        self.active_connections[conversation_id].append(websocket)
        
        logger.info(
            "WebSocket connected", 
            conversation_id=conversation_id,
            total_connections=len(self.active_connections[conversation_id])
        )
    
    def disconnect(self, websocket: WebSocket, conversation_id: str):
        """Remove a WebSocket connection"""
        if conversation_id in self.active_connections:
            if websocket in self.active_connections[conversation_id]:
                self.active_connections[conversation_id].remove(websocket)
                
                # Clean up empty conversation entries
                if not self.active_connections[conversation_id]:
                    del self.active_connections[conversation_id]
                
                logger.info(
                    "WebSocket disconnected",
                    conversation_id=conversation_id,
                    remaining_connections=len(self.active_connections.get(conversation_id, []))
                )
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error("Failed to send personal message", error=str(e))
    
    async def broadcast_to_conversation(self, message: dict, conversation_id: str):
        """Send a message to all connections for a specific conversation"""
        if conversation_id not in self.active_connections:
            logger.warning("No active connections for conversation", conversation_id=conversation_id)
            return
        
        message_json = json.dumps(message)
        disconnected_connections = []
        
        for websocket in self.active_connections[conversation_id]:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.error(
                    "Failed to broadcast message", 
                    conversation_id=conversation_id,
                    error=str(e)
                )
                disconnected_connections.append(websocket)
        
        # Clean up failed connections
        for websocket in disconnected_connections:
            self.disconnect(websocket, conversation_id)
    
    async def broadcast_to_all(self, message: dict):
        """Send a message to all active connections"""
        for conversation_id in list(self.active_connections.keys()):
            await self.broadcast_to_conversation(message, conversation_id)
    
    def get_connection_count(self, conversation_id: str = None) -> int:
        """Get the number of active connections"""
        if conversation_id:
            return len(self.active_connections.get(conversation_id, []))
        
        return sum(len(connections) for connections in self.active_connections.values())
    
    def get_active_conversations(self) -> List[str]:
        """Get list of conversation IDs with active connections"""
        return list(self.active_connections.keys())