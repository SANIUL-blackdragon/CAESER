from fastapi.testclient import TestClient
from api.main import app
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.mark.asyncio
async def test_analyze_endpoint():
    payload = {
        "product_name": "Test Product",
        "description": "Test description",
        "tags": "test,product",
        "sources": "reddit",
        "target_area": "Global",
        "locations": "Earth",
        "gender": "All"
    }
    with patch("api.main.run_scrapy.delay") as mock_delay:
        mock_task = MagicMock()
        mock_task.id = "fake_task_id"
        mock_delay.return_value = mock_task

        resp = client.post("/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["task_id"] == "fake_task_id"

@pytest.mark.asyncio
async def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}