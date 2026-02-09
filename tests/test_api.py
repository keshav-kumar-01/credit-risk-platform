"""
Unit tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add api to path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "api"))

from main import app, model

@pytest.fixture(scope="module")
def client():
    """Create a test client that triggers lifespan events"""
    with TestClient(app) as c:
        yield c


def test_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_single_prediction(client):
    """Test single prediction endpoint"""
    payload = {
        "age": 30,
        "credit_amount": 5000,
        "duration": 24,
        "installment_rate": 4
    }
    
    response = client.post("/predict", json=payload)
    if response.status_code != 200:
        print(f"\nResponse Error: {response.json()}")
    assert response.status_code == 200
    
    data = response.json()
    assert "decision" in data
    assert data["decision"] in ["APPROVED", "DECLINED"]
    assert "probability" in data
    assert 0 <= data["probability"] <= 1
    assert "top_factors" in data
    assert len(data["top_factors"]) > 0


def test_batch_prediction(client):
    """Test batch prediction endpoint"""
    payload = {
        "applications": [
            {
                "age": 30,
                "credit_amount": 5000,
                "duration": 24,
                "installment_rate": 4
            },
            {
                "age": 45,
                "credit_amount": 10000,
                "duration": 36,
                "installment_rate": 3
            }
        ]
    }
    
    response = client.post("/batch-predict", json=payload)
    if response.status_code != 200:
        print(f"\nResponse Error: {response.json()}")
    assert response.status_code == 200
    
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 2
    assert data["total"] == 2


def test_model_info(client):
    """Test model info endpoint"""
    response = client.get("/model-info")
    assert response.status_code == 200
    
    data = response.json()
    assert "model_name" in data
    assert "performance" in data


def test_invalid_input(client):
    """Test validation with invalid input"""
    payload = {
        "age": -5,  # Invalid age
        "credit_amount": 5000,
        "duration": 24,
        "installment_rate": 4
    }
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
