# tests/conftest.py
import os, sys, json, dotenv
from unittest.mock import patch, MagicMock
import pytest

# 1. make `api` importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. load .env once
dotenv.load_dotenv(dotenv.find_dotenv())

@pytest.fixture(autouse=True, scope="session")
def mock_secrets_and_env():
    """
    In-memory AWS Secrets Manager mock that returns the environment variable
    value for every requested secret.  This keeps the *real* .env values
    while still allowing the test suite to run without AWS credentials.
    """
    def _get_secret(SecretId, **kw):
        # map secret name -> env var name (drop prefix + snake-case)
        env_map = {
            "caeser-db-url":       os.getenv("DB_PATH"),
            "caeser-redis-url":    os.getenv("REDIS_URL"),
            "qloo-api-key":        os.getenv("QLOO_API_KEY"),
            "openrouter-key":      os.getenv("OPENROUTER_API_KEY"),
            "discord_webhook":     os.getenv("DISCORD_WEBHOOK_URL"),
            "slack_webhook":       os.getenv("SLACK_WEBHOOK_URL"),
            "email_host":          os.getenv("EMAIL_HOST"),
            "email_port":          os.getenv("EMAIL_PORT"),
            "email_user":          os.getenv("EMAIL_USER"),
            "email_password":      os.getenv("EMAIL_PASSWORD"),
            "email_recipient":     os.getenv("EMAIL_RECIPIENT"),
        }
        val = env_map.get(SecretId, "") or ""
        return {"SecretString": json.dumps(val)}

    mock = MagicMock()
    mock.get_secret_value.side_effect = _get_secret
    with patch("boto3.client", return_value=mock):
        yield