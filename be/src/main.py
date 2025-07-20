"""
FastAPI main application for LlamaIndex Presales AI System
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import uvicorn

from .config import get_settings
from .database import init_db
from .websocket_manager import WebSocketManager

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting LlamaIndex Presales AI System")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down LlamaIndex Presales AI System")


# Initialize FastAPI application
app = FastAPI(
    title="LlamaIndex Presales AI System",
    description="Transform customer conversations into comprehensive proposal packages",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
websocket_manager = WebSocketManager()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "presales-ai-backend"}


@app.get("/api/status")
async def api_status():
    """API status with configuration info"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "llm_model": settings.default_llm_model,
        "embedding_model": settings.default_embedding_model,
        "debug": settings.debug
    }


@app.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    """WebSocket endpoint for real-time pipeline updates"""
    await websocket_manager.connect(websocket, conversation_id)
    logger.info("WebSocket connection established", conversation_id=conversation_id)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            logger.debug("Received WebSocket message", conversation_id=conversation_id, data=data)
            
            # Echo back for testing - will be replaced with actual pipeline integration
            await websocket_manager.send_personal_message(
                {"type": "echo", "data": data}, 
                websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, conversation_id)
        logger.info("WebSocket connection closed", conversation_id=conversation_id)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for better error logging"""
    logger.error("Unhandled exception", exc_info=exc, path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level
    )