import os
import logging
from datetime import datetime, timedelta
from typing import Optional

import asyncpg

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

async def _init_connections() -> None:
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS data_quality (
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    source TEXT NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS llm_data_quality (
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
        logger.info("PostgreSQL connected and data_quality table ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create table: {e}")
        pg_pool = None

async def log_data_quality(metric: str, value: float, source: str):
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot log data quality.")
        return
    try:
        async with pg_pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO data_quality (metric, value, source, timestamp) VALUES ($1, $2, $3, NOW())",
                metric, value, source
            )
        logger.info(f"Logged data quality: {metric} = {value} for {source}")
    except Exception as e:
        logger.error(f"Failed to log data quality to PostgreSQL: {e}")

async def check_data_quality():
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot check data quality.")
        return {"success": False, "message": "Database not connected"}

    metrics = {}
    try:
        async with pg_pool.acquire() as conn:
            # Check missing values in social_data
            missing_values = await conn.fetchval("SELECT COUNT(*) FROM social_data WHERE text IS NULL OR text = ''")
            metrics['missing_values'] = {'value': missing_values, 'source': 'social_data'}
            await log_data_quality('missing_values', missing_values, 'social_data')
            
            # Check feed freshness
            latest_timestamp_str = await conn.fetchval("SELECT MAX(timestamp) FROM social_data")
            freshness = 0.0
            if latest_timestamp_str:
                latest_timestamp = datetime.fromisoformat(latest_timestamp_str.isoformat())
                freshness = (datetime.now() - latest_timestamp).total_seconds() / 3600
            metrics['freshness'] = {'value': freshness, 'source': 'social_data'}
            await log_data_quality('freshness', freshness, 'social_data')
            
            # Check API errors (from llm_data_quality for now)
            api_errors = await conn.fetchval("SELECT COUNT(*) FROM llm_data_quality WHERE metric = 'errors' AND value = 1.0")
            metrics['api_errors'] = {'value': api_errors, 'source': 'llm_service'}
            await log_data_quality('api_errors', api_errors, 'llm_service')
            
        return {
            "success": True,
            "data": metrics,
            "message": "Data quality metrics retrieved"
        }
    except Exception as e:
        logger.error(f"Failed to check data quality from PostgreSQL: {e}")
        return {"success": False, "message": f"Failed to retrieve data quality: {e}"}

async def check_data_quality_async():
    return await check_data_quality()

async def init_data_quality_service():
    await _init_connections()
