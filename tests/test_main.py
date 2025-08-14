"""
Test main application endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_llm_generate_sync(client, sample_llm_request):
    """Test synchronous LLM generation endpoint"""
    response = client.post("/v1/generate", json=sample_llm_request)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "model" in data
    assert "choices" in data
    assert len(data["choices"]) > 0