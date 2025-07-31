import random
from typing import Dict
import logging
import re
from collections import defaultdict
import sqlite3
import os
from textblob import TextBlob
from datetime import datetime, timedelta
import asyncio

# Enhanced emoji mapping with fallback
EMOJI_MAP = defaultdict(lambda: 0.0, {
    "😊": 0.8, "😢": -0.8, "😍": 0.9, "😠": -0.9, "😐": 0.0,
    "👍": 0.7, "👎": -0.7, "🔥": 0.85, "💯": 0.9, "👀": 0.3
})
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def get_categories() -> dict:
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.execute("SELECT category_name, keywords FROM categories")
        rows = cur.fetchall()
        conn.close()
        if not rows:
            return {
                "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
                "electronics": ["electronics", "gadgets", "tech", "devices"],
                "fashion": ["fashion", "clothing", "apparel", "style"]
            }
        return {row[0]: [kw.strip() for kw in row[1].split(",")] for row in rows}
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching categories: {e}")
        return {
            "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
            "electronics": ["electronics", "gadgets", "tech", "devices"],
            "fashion": ["fashion", "clothing", "apparel", "style"]
        }

category_keywords = get_categories()

# Cultural keywords for bonus scoring
CULTURAL_KEYWORDS = ["hype", "trend", "viral", "drop", "exclusive", "limited", "collab"]
# Psychographic vectors
PSYCHO_VEC = {
    "enthusiasm": lambda s: abs(s),
    "virality": lambda s: s * 1.2 if s > 0.5 else s,
    "controversy": lambda s: abs(s) * 0.8 if s < -0.3 else 0
}

def validate_insights(insights: Dict) -> None:
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    if not isinstance(insights["data"], dict):
        logger.error("Insights data must be a dictionary")
        raise ValueError("Insights data must be a dictionary")

def save_hype_score(score: float, category: str, location: str, sentiment: float, product_name: str | None = None) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hype_scores (score, category, location, sentiment, product_name, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (score, category or "", location or "", sentiment, product_name or ""))
    conn.commit()
    conn.close()

def get_previous_hype_score(category: str, location: str, product_name: str | None = None) -> tuple:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT score, sentiment FROM hype_scores 
        WHERE category = ? AND location = ?
    """
    params = [category or "", location or ""]
    if product_name:
        query += " AND product_name = ?"
        params.append(product_name or "")
    query += " ORDER BY created_at DESC LIMIT 1 OFFSET 1"
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

def get_hourly_sentiment_change(category: str, location: str, product_name: str | None = None) -> float:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT sentiment, created_at FROM hype_scores 
        WHERE category = ? AND location = ? AND created_at > ?
    """
    params = [category or "", location or "", (datetime.now() - timedelta(hours=1)).isoformat()]
    if product_name:
        query += " AND product_name = ?"
        params.append(product_name or "")
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    if len(rows) < 2:
        return 0.0
    latest_sentiment, prev_sentiment = rows[-1][0], rows[0][0]
    return ((latest_sentiment - prev_sentiment) / prev_sentiment * 100) if prev_sentiment != 0 else 0.0

def get_social_data(category: str, days: int = 7) -> list:
    keywords = category_keywords.get(category.lower() if category else "", [category or ""])
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"""
        SELECT text 
        FROM social_data 
        WHERE ({' OR '.join(['text LIKE ?' for _ in keywords])})
        AND timestamp > datetime('now', '-{days} days')
    """
    cursor.execute(query, tuple(f"%{kw}%" for kw in keywords))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def emoji_to_sentiment(text: str) -> float:
    scores = [EMOJI_MAP[ch] for ch in text if ch in EMOJI_MAP]
    return sum(scores) / (len(scores) or 1)

def scrub_pii(text: str) -> str:
    return EMAIL_REGEX.sub('', text or "")

def calculate_hype_score(insights: Dict, category: str, location: str, threshold: float = 20.0, product_name: str | None = None) -> Dict:
    validate_insights(insights)
    
    try:
        entities = insights["data"].get("entities", [])
        popularity = sum(entity["properties"].get("popularity", 0.5) for entity in entities) / len(entities) if entities else 0.5
        trend_factor = insights["data"].get("trend", 1.0)
        base_score = popularity * 100 * trend_factor
        
        historical_noise = get_historical_noise(category, location, product_name)
        hype_score = max(0.0, min(100.0, base_score + historical_noise))
        
        social_texts = get_social_data(category)
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
        
        previous_score, previous_sentiment = get_previous_hype_score(category, location, product_name)
        save_hype_score(hype_score, category, location, sentiment_score, product_name)
        
        change_detected = False
        change_percent = 0.0
        if previous_score is not None:
            change_percent = ((hype_score - previous_score) / previous_score) * 100
            change_detected = abs(change_percent) > threshold
        
        hourly_sentiment_change = get_hourly_sentiment_change(category, location, product_name)
        
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

def get_historical_noise(category: str, location: str, product_name: str = None) -> float:
    """
    Fetch historical noise data based on category, location, and product name.
    This function should be implemented to fetch real historical data.
    For now, it returns a placeholder value.
    """
    return 0.0

async def calculate_hype_score_async(insights, category, location, threshold=20.0, product_name: str | None = None):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, calculate_hype_score, insights, category or "", location or "", threshold, product_name or ""
    )
