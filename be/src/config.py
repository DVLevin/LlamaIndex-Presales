"""
Configuration management for LlamaIndex Presales AI System
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Keys
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    jina_api_key: str = Field(..., env="JINA_API_KEY")
    
    # LLM Configuration  
    default_llm_model: str = Field("moonshotai/kimi-k2", env="DEFAULT_LLM_MODEL")
    default_embedding_model: str = Field("jina-embeddings-v2-base-en", env="DEFAULT_EMBEDDING_MODEL")
    default_reranker_model: str = Field("jina-reranker-v1-base-en", env="DEFAULT_RERANKER_MODEL")
    
    # Database Configuration
    database_url: str = Field("postgresql://user:password@localhost:5432/presales_ai", env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # Server Configuration
    backend_host: str = Field("0.0.0.0", env="BACKEND_HOST")
    backend_port: int = Field(8000, env="BACKEND_PORT")
    frontend_url: str = Field("http://localhost:5173", env="FRONTEND_URL")
    
    # Development Settings
    debug: bool = Field(True, env="DEBUG")
    log_level: str = Field("info", env="LOG_LEVEL")
    
    # File Storage
    upload_dir: str = Field("./uploads", env="UPLOAD_DIR")
    output_dir: str = Field("./generated_docs", env="OUTPUT_DIR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance"""
    return settings