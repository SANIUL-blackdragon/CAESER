import pytest
from api.services.predict_trend import predict_trend
import sqlite3
from unittest.mock import patch

@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE social_data (
            text TEXT, likes INTEGER, source TEXT, timestamp TEXT
        )
    """)
    conn.execute("""
        INSERT INTO social_data (text, likes, source, timestamp)
        VALUES ('test product', 100, 'google_trends', '2025-07-29T00:00:00'),
               ('test product', 150, 'google_trends', '2025-07-30T00:00:00'),
               ('test product', 200, 'google_trends', '2025-07-31T00:00:00')
    """)
    conn.commit()
    with patch("api.services.predict_trend.sqlite3.connect", return_value=conn):
        yield conn
    conn.close()

def test_predict_trend_success(mock_db):
    result = predict_trend("test product", "test")
    assert result["success"] is True
    assert "predicted_peak_days" in result
    assert "confidence" in result
    assert result["confidence"] > 0

def test_predict_trend_no_data():
    with patch("api.services.predict_trend.sqlite3.connect", return_value=sqlite3.connect(":memory:")):
        result = predict_trend("unknown product", "unknown")
        assert result["success"] is False
        assert "message" in result