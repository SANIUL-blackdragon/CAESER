import sqlite3
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def log_data_quality(metric: str, value: float, source: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO data_quality (metric, value, source, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """, (metric, value, source))
    conn.commit()
    conn.close()
    logger.info(f"Logged data quality: {metric} = {value} for {source}")

def check_data_quality():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    metrics = {}
    
    # Check missing values in social_data
    cursor.execute("SELECT COUNT(*) FROM social_data WHERE text IS NULL OR text = ''")
    missing_values = cursor.fetchone()[0]
    metrics['missing_values'] = {'value': missing_values, 'source': 'social_data'}
    log_data_quality('missing_values', missing_values, 'social_data')
    
    # Check feed freshness
    cursor.execute("SELECT MAX(timestamp) FROM social_data")
    latest_timestamp = cursor.fetchone()[0]
    freshness = 0 if not latest_timestamp else (datetime.now() - datetime.fromisoformat(latest_timestamp)).total_seconds() / 3600
    metrics['freshness'] = {'value': freshness, 'source': 'social_data'}
    log_data_quality('freshness', freshness, 'social_data')
    
    # Check API errors (from llm_data_quality for now)
    cursor.execute("SELECT COUNT(*) FROM llm_data_quality WHERE metric = 'errors' AND value = 1.0")
    api_errors = cursor.fetchone()[0]
    metrics['api_errors'] = {'value': api_errors, 'source': 'llm_service'}
    log_data_quality('api_errors', api_errors, 'llm_service')
    
    conn.close()
    return {
        "success": True,
        "data": metrics,
        "message": "Data quality metrics retrieved"
    }