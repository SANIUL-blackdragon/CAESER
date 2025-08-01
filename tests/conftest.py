# tests/conftest.py
import os, sys, json, dotenv
from unittest.mock import patch, MagicMock
import pytest

# 1. make `api` importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. load .env once
dotenv.load_dotenv(dotenv.find_dotenv())

@pytest.fixture
def client():
    from api.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)