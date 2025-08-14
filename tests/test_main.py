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


def test_ping(client):
    """Test ping endpoint"""
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["pong"] is True


def test_posts_list_empty(client):
    """Test posts list when empty"""
    response = client.get("/api/v1/posts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_post(client, sample_post_data):
    """Test creating a post"""
    response = client.post("/api/v1/posts/", json=sample_post_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_post_data["title"]
    assert data["content"] == sample_post_data["content"]
    assert "id" in data


def test_get_post(client):
    """Test getting a specific post"""
    # First create a post
    post_data = {
        "title": "Test Get Post", 
        "content": "This is a test post for getting",
        "author": "Test Author"
    }
    create_response = client.post("/api/v1/posts/", json=post_data)
    created_post = create_response.json()
    post_id = created_post["id"]
    
    # Then get it
    response = client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == post_data["title"]


def test_get_nonexistent_post(client):
    """Test getting a non-existent post"""
    response = client.get("/api/v1/posts/99999")
    assert response.status_code == 404