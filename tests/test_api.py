from fastapi.testclient import TestClient
from api.main import app
import pytest
import json
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_secrets():
    """Mocks AWS Secrets Manager client and its return values."""
    mock_secrets_manager = MagicMock()

    def get_secret_value(SecretId, **kwargs):
        secrets = {
            "caeser-db-url": "postgresql+asyncpg://testuser:testpass@localhost:5432/testdb",
            "caeser-redis-url": "redis://localhost:6379/1",
            "qloo-api-key": "fake-qloo-key",
            "openrouter-key": "fake-openrouter-key",
            "discord_webhook": "https://fake-discord-webhook.com",
            "slack_webhook": "https://fake-slack-webhook.com",
            "email_host": "smtp.fakeserver.com",
            "email_port": "587",
            "email_user": "fake@user.com",
            "email_password": "fakepassword",
            "email_recipient": "recipient@fake.com"
        }
        secret_string = json.dumps(secrets.get(SecretId, ""))
        return {"SecretString": secret_string}

    mock_secrets_manager.get_secret_value.side_effect = get_secret_value

    with patch('boto3.client', return_value=mock_secrets_manager) as mock_boto_client:
        yield mock_boto_client


client = TestClient(app)

@pytest.mark.asyncio
async def test_analyze_endpoint():
    # Test successful analysis
    payload = {
        "product_name": "Test Product",
        "description": "This is a test product",
        "tags": "test, product",
        "sources": "reddit",
        "target_area": "Test Area",
        "locations": "Test Location",
        "gender": "All"
    }
    # Mock the celery task
    with patch('api.main.run_scrapy.delay') as mock_delay:
        mock_task = MagicMock()
        mock_task.id = "fake_task_id"
        mock_delay.return_value = mock_task
        response = client.post("/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "hype_score" in data
    assert "trend_prediction" in data
    assert data["task_id"] == "fake_task_id"


@pytest.mark.asyncio
async def test_analyze_endpoint_invalid_input():
    # Test error handling with incomplete input
    payload = {"product_name": "Test Product"}  # Missing required fields
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422  # FastAPI validation error


@pytest.mark.asyncio
async def test_health_endpoint():
    # Test basic health check
    with patch('sqlalchemy.ext.asyncio.AsyncEngine.begin') as mock_begin:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
