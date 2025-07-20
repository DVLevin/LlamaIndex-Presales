"""
Tests for configuration management
"""
import pytest
from unittest.mock import patch
import os

import sys
sys.path.append('.')
sys.path.append('..')

from be.src.config import Settings, get_settings


def test_settings_defaults():
    """Test default configuration values"""
    with patch.dict(os.environ, {
        "OPENROUTER_API_KEY": "test-openrouter-key",
        "JINA_API_KEY": "test-jina-key"
    }):
        settings = Settings()
        
        # Test required fields have values
        assert settings.openrouter_api_key == "test-openrouter-key"
        assert settings.jina_api_key == "test-jina-key"
        
        # Test defaults
        assert settings.default_llm_model == "moonshotai/kimi-k2"
        assert settings.default_embedding_model == "jina-embeddings-v2-base-en"
        assert settings.default_reranker_model == "jina-reranker-v1-base-en"
        assert settings.backend_host == "0.0.0.0"
        assert settings.backend_port == 8000
        assert settings.debug is True
        assert settings.log_level == "info"


def test_settings_from_environment():
    """Test configuration from environment variables"""
    test_env = {
        "OPENROUTER_API_KEY": "env-openrouter-key",
        "JINA_API_KEY": "env-jina-key",
        "DEFAULT_LLM_MODEL": "custom/model",
        "BACKEND_PORT": "9000",
        "DEBUG": "false"
    }
    
    with patch.dict(os.environ, test_env):
        settings = Settings()
        
        assert settings.openrouter_api_key == "env-openrouter-key"
        assert settings.jina_api_key == "env-jina-key"
        assert settings.default_llm_model == "custom/model"
        assert settings.backend_port == 9000
        assert settings.debug is False


def test_get_settings():
    """Test settings getter function"""
    settings = get_settings()
    assert isinstance(settings, Settings)
    # Just verify the function returns a Settings instance
    # The actual values come from .env which are real secrets


def test_database_url_format():
    """Test database URL configuration"""
    with patch.dict(os.environ, {
        "OPENROUTER_API_KEY": "test-key",
        "JINA_API_KEY": "test-jina-key",
        "DATABASE_URL": "postgresql://user:pass@db:5432/testdb"
    }):
        settings = Settings()
        assert settings.database_url == "postgresql://user:pass@db:5432/testdb"


def test_file_storage_paths():
    """Test file storage path configuration"""
    with patch.dict(os.environ, {
        "OPENROUTER_API_KEY": "test-key", 
        "JINA_API_KEY": "test-jina-key",
        "UPLOAD_DIR": "/custom/uploads",
        "OUTPUT_DIR": "/custom/output"
    }):
        settings = Settings()
        assert settings.upload_dir == "/custom/uploads"
        assert settings.output_dir == "/custom/output"


@pytest.mark.skipif(not os.path.exists(".env"), reason=".env file not found")
def test_settings_load_from_dotenv():
    """Test loading settings from .env file (if exists)"""
    # This test only runs if .env file exists
    settings = Settings()
    
    # Should load from .env without errors
    assert settings.openrouter_api_key is not None
    assert settings.jina_api_key is not None