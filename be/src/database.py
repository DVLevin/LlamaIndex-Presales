"""
Database configuration and models for LlamaIndex Presales AI System
"""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4, UUID

from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import sessionmaker, relationship
import structlog

from .config import get_settings

logger = structlog.get_logger()
settings = get_settings()

# Database engine and session
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug
)

AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()


class Conversation(Base):
    """Customer conversation and transcript storage"""
    __tablename__ = "conversations"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    original_transcript = Column(Text, nullable=False)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(50), default="created")
    
    # Relationships
    pipeline_executions = relationship("PipelineExecution", back_populates="conversation")
    uploaded_files = relationship("UploadedFile", back_populates="conversation")


class PipelineExecution(Base):
    """Pipeline execution tracking and configuration"""
    __tablename__ = "pipeline_executions"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(PGUUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    llm_model = Column(String(100), nullable=False)
    agent_config = Column(JSON, default=dict)
    status = Column(String(50), default="pending")
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    execution_log = Column(JSON, default=dict)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="pipeline_executions")
    agent_steps = relationship("AgentStep", back_populates="execution")
    generated_documents = relationship("GeneratedDocument", back_populates="execution")


class AgentStep(Base):
    """Individual agent step execution tracking"""
    __tablename__ = "agent_steps"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    execution_id = Column(PGUUID(as_uuid=True), ForeignKey("pipeline_executions.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    step_number = Column(Integer, nullable=False)
    input_data = Column(Text, nullable=True)
    output_data = Column(Text, nullable=True)
    metadata = Column(JSON, default=dict)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending")
    
    # Relationships
    execution = relationship("PipelineExecution", back_populates="agent_steps")


class GeneratedDocument(Base):
    """Generated documents and artifacts"""
    __tablename__ = "generated_documents"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    execution_id = Column(PGUUID(as_uuid=True), ForeignKey("pipeline_executions.id"), nullable=False)
    document_type = Column(String(100), nullable=False)  # problem_overview, process_overview, etc.
    file_path = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)  # Store content for search/preview
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    execution = relationship("PipelineExecution", back_populates="generated_documents")


class UploadedFile(Base):
    """Uploaded files tracking"""
    __tablename__ = "uploaded_files"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(PGUUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="uploaded_files")


async def init_db():
    """Initialize database tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def get_db() -> AsyncSession:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Database utility functions
async def create_conversation(
    title: str, 
    transcript: str, 
    metadata: Optional[Dict[str, Any]] = None
) -> Conversation:
    """Create a new conversation record"""
    async with AsyncSessionLocal() as session:
        conversation = Conversation(
            title=title,
            original_transcript=transcript,
            metadata=metadata or {}
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation


async def create_pipeline_execution(
    conversation_id: UUID,
    llm_model: str,
    agent_config: Optional[Dict[str, Any]] = None
) -> PipelineExecution:
    """Create a new pipeline execution record"""
    async with AsyncSessionLocal() as session:
        execution = PipelineExecution(
            conversation_id=conversation_id,
            llm_model=llm_model,
            agent_config=agent_config or {},
            started_at=datetime.utcnow(),
            status="running"
        )
        session.add(execution)
        await session.commit()
        await session.refresh(execution)
        return execution