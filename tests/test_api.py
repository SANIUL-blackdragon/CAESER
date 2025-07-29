from fastapi.testclient import TestClient
from api.main import app
import pytest

client = TestClient(app)

@pytest.mark.asyncio
async def test_analyze_endpoint():
    # Test successful analysis
    payload = {
        "product_name": "Test Product",
        "description": "This is a test product",
        "tags": "test, product",
        "target_area": "Test Area",
        "locations": "Test Location",
        "gender": "All"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "hype_score" in data
    assert "trend_prediction" in data

@pytest.mark.asyncio
async def test_analyze_endpoint_invalid_input():
    # Test error handling with incomplete input
    payload = {"product_name": "Test Product"}  # Missing required fields
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200  # FastAPI returns 200 with error in body
    data = response.json()
    assert data["success"] is False
    assert "message" in data

@pytest.mark.asyncio
async def test_health_endpoint():
    # Test basic health check
    response = client.get("/health")
    assert response.status_code == 200