"""
Streamlit Application Configuration
Secure API key handling and app settings with .env.local support
"""
import os
from typing import Dict, Any
import streamlit as st
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env.local if it exists
env_local_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env.local')
if os.path.exists(env_local_path):
    load_dotenv(env_local_path)
    
# Also load from .env as fallback
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)


class AppConfig(BaseModel):
    """Application configuration with validation"""
    
    # API Configuration
    openrouter_api_key: str = Field(default="", description="OpenRouter API key for LLM access")
    jina_api_key: str = Field(default="", description="Jina AI API key for embeddings/rerankers")
    
    # Model Configuration
    available_models: Dict[str, str] = Field(
        default={
            "gpt-oss-120b": "openai/gpt-oss-120b",
            "claude-3.7-sonnet": "anthropic/claude-3.7-sonnet",
            "gpt-4o": "openai/gpt-4o", 
            "deepseek-coder-v2": "deepseek/deepseek-coder-v2",
            "gemini-2.5-flash": "google/gemini-2.5-flash-lite"
        },
        description="Available LLM models"
    )
    
    # Agent-Specific Model Mappings (unified configuration)  
    agent_models: Dict[str, str] = Field(
        default={
            "conversa": "openai/gpt-oss-120b",         # Unified model for all agents
            "conny": "openai/gpt-oss-120b",            # Unified model for all agents
            "prody": "openai/gpt-oss-120b",            # Unified model for all agents
            "preston": "openai/gpt-oss-120b",          # Unified model for all agents
            "marketing": "openai/gpt-oss-120b"         # Unified model for all agents
        },
        description="Agent-specific model mappings"
    )
    
    # Upload Configuration
    max_file_size_mb: int = Field(default=50, description="Maximum file upload size in MB")
    allowed_file_types: list = Field(
        default=["txt", "docx", "pdf", "md"],
        description="Allowed file types for upload"
    )
    
    # Pipeline Configuration
    max_processing_time_minutes: int = Field(default=10, description="Maximum pipeline processing time")
    enable_real_time_updates: bool = Field(default=True, description="Enable real-time pipeline updates")


def load_config() -> AppConfig:
    """Load configuration with API keys from session state or environment"""
    
    # Try to get API keys from various sources
    openrouter_key = (
        st.session_state.get("openrouter_api_key", "") or 
        os.getenv("OPENROUTER_API_KEY", "")
    )
    
    jina_key = (
        st.session_state.get("jina_api_key", "") or 
        os.getenv("JINA_API_KEY", "")  
    )
    
    return AppConfig(
        openrouter_api_key=openrouter_key,
        jina_api_key=jina_key
    )


def save_api_keys(openrouter_key: str, jina_key: str) -> None:
    """Securely save API keys to session state"""
    st.session_state["openrouter_api_key"] = openrouter_key
    st.session_state["jina_api_key"] = jina_key
    st.session_state["config_updated"] = True


def validate_api_keys(config: AppConfig) -> Dict[str, bool]:
    """Validate API key configuration"""
    return {
        "openrouter": bool(config.openrouter_api_key and config.openrouter_api_key.startswith("sk-or-v1-")),
        "jina": bool(config.jina_api_key and len(config.jina_api_key) > 20)
    }


def initialize_session_state():
    """Initialize session state variables"""
    if "pipeline_state" not in st.session_state:
        st.session_state.pipeline_state = "idle"
    
    if "current_transcript" not in st.session_state:
        st.session_state.current_transcript = None
        
    if "generated_documents" not in st.session_state:
        st.session_state.generated_documents = {}
        
    if "processing_progress" not in st.session_state:
        st.session_state.processing_progress = 0
        
    if "current_agent" not in st.session_state:
        st.session_state.current_agent = ""