import random
from typing import Dict
import logging
import sqlite3
import os
from textblob import TextBlob
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

category_keywords = {
    "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
    "electronics": ["electronics", "gadgets", "tech", "devices"],
    "fashion": ["fashion", "clothing", "apparel", "style"]
}

def validate_insights(insights: Dict) -> None:
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    if not isinstance(insights["data"], dict):
        logger.error("Insights data must be a dictionary")
        raise ValueError("Insights data must be a dictionary")

def save_hype_score(score: float, category: str, location: str, sentiment: float, product_name: str = None) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hype_scores (score, category, location, sentiment, product_name, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (score, category, location, sentiment, product_name))
    conn.commit()
    conn.close()

def get_previous_hype_score(category: str, location: str, product_name: str = None) -> tuple:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT score, sentiment FROM hype_scores 
        WHERE category = ? AND location = ?
    """
    params = [category, location]
    if product_name:
        query += " AND product_name = ?"
        params.append(product_name)
    query += " ORDER BY created_at DESC LIMIT 1 OFFSET 1"
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

def get_hourly_sentiment_change(category: str, location: str, product_name: str = None) -> float:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT sentiment, created_at FROM hype_scores 
        WHERE category = ? AND location = ? AND created_at > ?
    """
    params = [category, location, (datetime.now() - timedelta(hours=1)).isoformat()]
    if product_name:
        query += " AND product_name = ?"
        params.append(product_name)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    if len(rows) < 2:
        return 0.0
    latest_sentiment, prev_sentiment = rows[-1][0], rows[0][0]
    return ((latest_sentiment - prev_sentiment) / prev_sentiment * 100) if prev_sentiment != 0 else 0.0

def get_social_data(category: str, days: int = 7) -> list:
    keywords = category_keywords.get(category.lower(), [category])
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

def calculate_hype_score(insights: Dict, category: str, location: str, threshold: float = 20.0, product_name: str = None) -> Dict:
    validate_insights(insights)
    
    try:
        entities = insights["data"].get("entities", [])
        popularity = sum(entity["properties"].get("popularity", 0.5) for entity in entities) / len(entities) if entities else 0.5
        trend_factor = insights["data"].get("trend", 1.0)
        base_score = popularity * 100 * trend_factor
        simulation_noise = random.uniform(-10, 10)
        hype_score = max(0.0, min(100.0, base_score + simulation_noise))
        
        social_texts = get_social_data(category)
        if social_texts:
            sentiment_score = sum(TextBlob(text).sentiment.polarity for text in social_texts) / len(social_texts)
            logger.info(f"Analyzed {len(social_texts)} social posts for sentiment")
        else:
            sentiment_score = 0.0
            logger.warning("No social data found for sentiment analysis")
        
        hype_score = min(100.0, hype_score * (1 + sentiment_score * 0.2))
        
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
            "message": "Hype score calculated with sentiment"
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
            "message": f"Failed to calculate hype score: {str(e)}"
        }