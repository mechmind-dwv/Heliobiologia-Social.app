# tests/conftest.py
import pytest
import sys
import os
from fastapi.testclient import TestClient

# Añadir el directorio app al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../app'))

from app.main import app

@pytest.fixture
def client():
    """Fixture para cliente de testing de FastAPI"""
    return TestClient(app)

@pytest.fixture
def sample_solar_data():
    """Datos solares de ejemplo para testing"""
    return {
        "solar_flares": [
            {
                "flrID": "TEST_001",
                "beginTime": "2024-01-01T12:00:00Z",
                "peakTime": "2024-01-01T12:15:00Z",
                "endTime": "2024-01-01T12:30:00Z",
                "classType": "M5.2",
                "sourceLocation": "N15E45"
            }
        ],
        "active_regions": 3,
        "sunspots": 45
    }

@pytest.fixture
def sample_social_data():
    """Datos sociales de ejemplo para testing"""
    return {
        "engagement_rate": 0.045,
        "sentiment_score": 0.78,
        "post_count": 150,
        "trending_topics": ["#ciencia", "#cosmos", "#conciencia"]
    }

@pytest.fixture
def mock_environment(monkeypatch):
    """Mock de variables de entorno para testing"""
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("NASA_API_KEY", "test_nasa_key")
    monkeypatch.setenv("FACEBOOK_ACCESS_TOKEN", "test_fb_token")
