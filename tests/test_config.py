"""
Test configuration module
"""
import pytest
from unittest.mock import patch
import os
from app.core.config import Settings


class TestSettings:
    """Test Settings configuration"""
    
    def test_default_settings(self):
        """Test default settings values"""
        settings = Settings()
        assert settings.PROJECT_NAME == "Unified LLM API(V1)"
        assert settings.VERSION == "0.1.1"
        assert settings.DATABASE_URL == "sqlite+aiosqlite:///./app.db"
    
    @patch.dict(os.environ, {"PROJECT_NAME": "Test Project"})
    def test_settings_from_env(self):
        """Test settings loading from environment variables"""
        settings = Settings()
        assert settings.PROJECT_NAME == "Test Project"
    
    def test_settings_validation(self):
        """Test settings validation"""
        # Settings should be created without errors
        settings = Settings()
        assert settings is not None
        assert hasattr(settings, 'SECRET_KEY')
        assert hasattr(settings, 'DATABASE_URL')