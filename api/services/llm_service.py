# api/services/llm_service.py
"""
LLM service
- async OpenRouter calls via AsyncOpenAI
- Redis-based request/response caching
- 100 % backward-compatible return shape
"""
import os
import json
import time
import sqlite3
import logging
import asyncio
import redis.asyncio as redis  # async-first client

from openai import AsyncOpenAI
from typing import Dict

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
DB_PATH            = os.getenv("DB_PATH", "./data/caeser.db")
REDIS_URL          = os.getenv("REDIS_URL", "redis://localhost:6379/0")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL           = "http://localhost:8000"
SITE_NAME          = "CAESER"

logger = logging.getLogger(__name__)

# async Redis client
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Async OpenAI client
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def sanitize_input(s: str) -> str:
    return s.strip()

def log_llm_data_quality(metric: str, value: float):
    """Persist metric in SQLite synchronously (fast)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO llm_data_quality (metric, value, timestamp) VALUES (?, ?, ?)",
        (metric, value, time.time()),
    )
    conn.commit()
    conn.close()

# -----------------------------------------------------------------------------
# Core async function (upgraded & minimal)
# -----------------------------------------------------------------------------
async def _get_prediction_async(product: Dict, insights: Dict, hype_score: float) -> Dict:
    """
    Ultra-lean async variant that performs the LLM call and caching logic.
    """
    cache_key = f"llm:{product.get('name','')}:{hash(json.dumps(product, sort_keys=True))}"

    # Try cache first
    if (cached := await redis_client.get(cache_key)):
        return json.loads(cached)

    # Build prompt
    prompt = f"""
    Analyze the following product and cultural insights to predict demand uplift and suggest a marketing strategy.
    Product: {sanitize_input(product.get('name',''))}
    Tags: {', '.join([sanitize_input(t) for t in product.get('tags',[])])}
    Description: {sanitize_input(product.get('description',''))}
    Target Market: {sanitize_input(product.get('location','Global'))}
    Age: {sanitize_input(product.get('age_range','All'))}
    Gender: {sanitize_input(product.get('gender','All'))}
    Cultural Insights: {insights.get('data',{})}
    Hype Score: {hype_score}
    Provide a response in JSON format with 'uplift' (percentage, float), 'strategy' (string), 'confidence' (float 0-1), and 'trend' (list of dicts with 'time' and 'demand').
    """

    try:
        start = time.time()
        resp = await client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}],
            timeout=30,
        )
        data = json.loads(resp.choices[0].message.content.strip())

        # Validate required keys
        required = {"uplift", "strategy", "confidence", "trend"}
        if not required.issubset(data):
            raise ValueError("Invalid LLM response format")

        # Add mock TikTok costs (backward compatibility)
        data["cpc"] = 1.0
        data["cpm"] = 5.0

        # Cache for 1 hour
        await redis_client.setex(cache_key, 3600, json.dumps({"success": True, "data": data}))

        # Log quality metrics
        log_llm_data_quality("confidence", data.get("confidence", 0.0))
        log_llm_data_quality("response_time", time.time() - start)

        return {"success": True, "data": data, "message": "Prediction generated successfully"}

    except Exception as e:
        logger.error("LLM request failed: %s", e)
        log_llm_data_quality("errors", 1.0)
        return {"success": False, "data": None, "message": f"LLM request failed: {e}"}

# -----------------------------------------------------------------------------
# Sync wrapper (100 % backward-compatible)
# -----------------------------------------------------------------------------
def get_prediction(product: Dict, insights: Dict, hype_score: float) -> Dict:
    """
    Legacy synchronous entry-point for all existing callers.
    Internally delegates to the async implementation.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:  # no loop in current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_get_prediction_async(product, insights, hype_score))

# -----------------------------------------------------------------------------
# Data-quality endpoint (unchanged)
# -----------------------------------------------------------------------------
def get_llm_data_quality() -> Dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT metric, AVG(value) as avg_value, COUNT(*) as count
        FROM llm_data_quality
        GROUP BY metric
        """
    )
    rows = cursor.fetchall()
    conn.close()
    metrics = {row[0]: {"avg_value": row[1], "count": row[2]} for row in rows}
    return {
        "success": True,
        "data": metrics,
        "message": "LLM data quality metrics retrieved",
    }