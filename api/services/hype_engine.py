import random
from typing import Dict, Optional, List
import logging
import re
from collections import defaultdict
import os
from textblob import TextBlob
from datetime import datetime, timedelta
import asyncio
import asyncpg

# Enhanced emoji mapping with fallback
EMOJI_MAP = defaultdict(lambda: 0.0, {
    "😊": 0.8, "😢": -0.8, "😍": 0.9, "😠": -0.9, "😐": 0.0,
    "👍": 0.7, "👎": -0.7, "🔥": 0.85, "💯": 0.9, "👀": 0.3
})
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POSTGRES_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

async def _init_connections() -> None:
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS hype_scores (
                    id SERIAL PRIMARY KEY,
                    score REAL,
                    sentiment REAL,
                    category TEXT,
                    location TEXT,
                    product_name TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """)
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS social_data (
                    id SERIAL PRIMARY KEY,
                    source TEXT,
                    text TEXT,
                    likes INTEGER,
                    timestamp TIMESTAMPTZ
                );
                """)
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    category_name TEXT PRIMARY KEY,
                    keywords TEXT
                );
                """
            )
        logger.info("PostgreSQL connected and hype_scores, social_data, categories tables ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create tables: {e}")
        pg_pool = None

async def get_categories_async() -> Dict[str, List[str]]:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot fetch categories.")
        return {
            "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
            "electronics": ["electronics", "gadgets", "tech", "devices"],
            "fashion": ["fashion", "clothing", "apparel", "style"]
        }
    try:
        async with pg_pool.acquire() as conn:
            rows = await conn.fetch("SELECT category_name, keywords FROM categories")
            if not rows:
                return {
                    "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
                    "electronics": ["electronics", "gadgets", "tech", "devices"],
                    "fashion": ["fashion", "clothing", "apparel", "style"]
                }
            return {row["category_name"]: [kw.strip() for kw in row["keywords"].split(",")] for row in rows}
    except Exception as e:
        logger.error(f"Database error while fetching categories: {e}")
        return {
            "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
            "electronics": ["electronics", "gadgets", "tech", "devices"],
            "fashion": ["fashion", "clothing", "apparel", "style"]
        }

# Cultural keywords for bonus scoring
CULTURAL_KEYWORDS = ["hype", "trend", "viral", "drop", "exclusive", "limited", "collab"]
# Psychographic vectors
PSYCHO_VEC = {
    "enthusiasm": lambda s: abs(s),
    "virality": lambda s: s * 1.2 if s > 0.5 else s,
    "controversy": lambda s: abs(s) * 0.8 if s < -0.3 else 0
}

def validate_insights(insights):
    if not insights or not isinstance(insights, list):
        print("Received insights:", insights)  # ← Add this
        raise ValueError("Invalid insights data")
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    if not isinstance(insights["data"], dict):
        logger.error("Insights data must be a dictionary")
        raise ValueError("Insights data must be a dictionary")

async def save_hype_score(score: float, category: str, location: str, sentiment: float, product_name: str | None = None) -> None:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot save hype score.")
        return
    try:
        async with pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO hype_scores (score, category, location, sentiment, product_name, created_at)
                VALUES ($1, $2, $3, $4, $5, NOW())
            """, score, category or "", location or "", sentiment, product_name or "")
    except Exception as e:
        logger.error(f"Failed to save hype score to PostgreSQL: {e}")

async def get_previous_hype_score(category: str, location: str, product_name: str | None = None) -> tuple:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot get previous hype score.")
        return (None, None)
    try:
        async with pg_pool.acquire() as conn:
            query = """
                SELECT score, sentiment FROM hype_scores 
                WHERE category = $1 AND location = $2
            """
            params = [category or "", location or ""]
            if product_name:
                query += " AND product_name = $3"
                params.append(product_name or "")
            query += " ORDER BY created_at DESC LIMIT 1 OFFSET 1"
            
            # Adjust parameter indexing for asyncpg
            if product_name:
                row = await conn.fetchrow(query, params[0], params[1], params[2])
            else:
                row = await conn.fetchrow(query, params[0], params[1])
            
            return (row["score"], row["sentiment"]) if row else (None, None)
    except Exception as e:
        logger.error(f"Failed to get previous hype score from PostgreSQL: {e}")
        return (None, None)

async def get_hourly_sentiment_change(category: str, location: str, product_name: str | None = None) -> float:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot get hourly sentiment change.")
        return 0.0
    try:
        async with pg_pool.acquire() as conn:
            query = """
                SELECT sentiment, created_at FROM hype_scores 
                WHERE category = $1 AND location = $2 AND created_at > NOW() - INTERVAL '1 hour'
            """
            params = [category or "", location or ""]
            if product_name:
                query += " AND product_name = $3"
                params.append(product_name or "")
            
            if product_name:
                rows = await conn.fetch(query, params[0], params[1], params[2])
            else:
                rows = await conn.fetch(query, params[0], params[1])
            
            if len(rows) < 2:
                return 0.0
            
            # Sort by created_at to ensure correct latest/oldest sentiment
            rows.sort(key=lambda r: r["created_at"])
            latest_sentiment = rows[-1]["sentiment"]
            oldest_sentiment = rows[0]["sentiment"]
            
            return ((latest_sentiment - oldest_sentiment) / oldest_sentiment * 100) if oldest_sentiment != 0 else 0.0
    except Exception as e:
        logger.error(f"Failed to get hourly sentiment change from PostgreSQL: {e}")
        return 0.0

async def get_social_data(category: str, days: int = 7) -> List[str]:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot get social data.")
        return []
    try:
        category_keywords = await get_categories_async() # Fetch categories asynchronously
        keywords = category_keywords.get(category.lower() if category else "", [category or ""])
        
        async with pg_pool.acquire() as conn:
            # Constructing dynamic WHERE clause for keywords
            where_clauses = [f"text ILIKE '%{kw}%'" for kw in keywords]
            query = f"""
                SELECT text 
                FROM social_data 
                WHERE ({' OR '.join(where_clauses)})
                AND timestamp > NOW() - INTERVAL '{days} days'
            """
            rows = await conn.fetch(query)
            return [row["text"] for row in rows]
    except Exception as e:
        logger.error(f"Failed to get social data from PostgreSQL: {e}")
        return []

def emoji_to_sentiment(text: str) -> float:
    scores = [EMOJI_MAP[ch] for ch in text if ch in EMOJI_MAP]
    return sum(scores) / (len(scores) or 1)

def scrub_pii(text: str) -> str:
    return EMAIL_REGEX.sub('', text or "")

async def calculate_hype_score(insights: Dict, category: str, location: str, threshold: float = 20.0, product_name: str | None = None) -> Dict:
    validate_insights(insights)
    
    try:
        entities = insights["data"].get("entities", [])
        popularity = sum(entity["properties"].get("popularity", 0.5) for entity in entities) / len(entities) if entities else 0.5
        trend_factor = insights["data"].get("trend", 1.0)
        base_score = popularity * 100 * trend_factor
        
        historical_noise = await get_historical_noise(category, location, product_name) # Make this async
        hype_score = max(0.0, min(100.0, base_score + historical_noise))
        
        social_texts = await get_social_data(category) # Make this async
        if social_texts:
            sentiment_score = sum(
                TextBlob(scrub_pii(text)).sentiment.polarity + emoji_to_sentiment(text) # type: ignore
                for text in social_texts
            ) / len(social_texts) if social_texts else 0.0
            logger.info(f"Analyzed {len(social_texts)} social posts for sentiment")
        else:
            sentiment_score = 0.0
            logger.warning("No social data found for sentiment analysis")
        
        hype_score = min(100.0, hype_score * (1 + sentiment_score * 0.2))
        
        cultural_bonus = sum(1 for k in CULTURAL_KEYWORDS if k in " ".join(social_texts).lower()) * 2
        psychographic = PSYCHO_VEC["enthusiasm"](sentiment_score)
        hype_score = min(100.0, hype_score + cultural_bonus + psychographic)
        
        scenario = {"price_drop": min(100.0, hype_score * 1.05)}
        cycle_phase = "growth" if hype_score > 50 else "decline"
        confidence_weight = min(1.0, (entities[0]["properties"].get("confidence", 0.5) if entities else 0.5) * 0.8 + 0.2)
        
        previous_score, previous_sentiment = await get_previous_hype_score(category, location, product_name) # Make this async
        await save_hype_score(hype_score, category, location, sentiment_score, product_name) # Make this async
        
        change_detected = False
        change_percent = 0.0
        if previous_score is not None:
            change_percent = ((hype_score - previous_score) / previous_score) * 100
            change_detected = abs(change_percent) > threshold
        
        hourly_sentiment_change = await get_hourly_sentiment_change(category, location, product_name) # Make this async
        
        logger.info(f"Calculated hype score: {hype_score:.2f}, Sentiment: {sentiment_score:.2f}, Change: {change_percent:.2f}%, Hourly Sentiment Change: {hourly_sentiment_change:.2f}%")
        return {
            "success": True,
            "averageScore": round(hype_score, 2),
            "sentiment": round(sentiment_score, 2),
            "change_detected": change_detected,
            "change_percent": round(change_percent, 2),
            "hourly_sentiment_change": round(hourly_sentiment_change, 2),
            "scenario": scenario,
            "cycle_phase": cycle_phase,
            "confidence_weight": round(confidence_weight, 2),
            "message": "Enhanced hype score calculated with cultural and psychographic factors"
        }
    except Exception as e:
        logger.error(f"Failed to calculate hype score: {str(e)}")
        return {
            "success": False, 
            "averageScore": 0.0, 
            "sentiment": 0.0, 
            "change_detected": False, 
            "change_percent": 0.0, 
            "hourly_sentiment_change": 0.0,
            "scenario": {},
            "cycle_phase": "unknown",
            "confidence_weight": 0.0,
            "message": f"Failed to calculate hype score: {str(e)}"
        }

async def get_historical_noise(category: str, location: str, product_name: str | None = None) -> float:
    """
    Fetch historical noise data based on category, location, and product name.
    This function should be implemented to fetch real historical data.
    For now, it returns a placeholder value.
    """
    return 0.0

async def calculate_hype_score_async(insights, category, location, threshold=20.0, product_name: str | None = None):
    return await calculate_hype_score(insights, category or "", location or "", threshold, product_name or "")

async def init_hype_engine_service():
    await _init_connections()