import random
from typing import Dict
import logging
import sqlite3
import os

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def validate_insights(insights: Dict) -> None:
    """Validate insights data structure.
    
    Args:
        insights (dict): Cultural insights from Qloo API.
    
    Raises:
        ValueError: If insights data is invalid.
    """
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    if not isinstance(insights["data"], dict):
        logger.error("Insights data must be a dictionary")
        raise ValueError("Insights data must be a dictionary")

def save_hype_score(score: float, category: str, location: str) -> None:
    """Save the current hype score to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hype_scores (score, category, location, created_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """, (score, category, location))
    conn.commit()
    conn.close()

def get_previous_hype_score(category: str, location: str) -> float:
    """Retrieve the most recent previous hype score from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT score FROM hype_scores 
        WHERE category = ? AND location = ?
        ORDER BY created_at DESC LIMIT 1 OFFSET 1
    """, (category, location))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def calculate_hype_score(insights: Dict, category: str, location: str, threshold: float = 20.0) -> Dict:
    """Calculate a hype score and check for significant changes.
    
    Args:
        insights (dict): Cultural insights from Qloo API.
        category (str): Product category.
        location (str): Geographic location.
        threshold (float): Percentage change threshold for alerts.
    
    Returns:
        Dict: Hype score with change detection results.
    """
    validate_insights(insights)
    
    try:
        entities = insights["data"].get("entities", [])
        if not entities:
            logger.warning("No entities found in insights data, using default popularity")
            popularity = 0.5
        else:
            popularity = sum(entity["properties"].get("popularity", 0.5) for entity in entities) / len(entities)
        
        trend_factor = insights["data"].get("trend", 1.0)
        base_score = popularity * 100 * trend_factor
        simulation_noise = random.uniform(-10, 10) # Simulate some variability
        # Ensure score is within 0-100 range
        if base_score < 0:
            base_score = 0
        elif base_score > 100:
            base_score = 100
        hype_score = max(0.0, min(100.0, base_score + simulation_noise))
        
        previous_score = get_previous_hype_score(category, location)
        save_hype_score(hype_score, category, location)
        
        change_detected = False
        change_percent = 0.0
        if previous_score is not None:
            change_percent = ((hype_score - previous_score) / previous_score) * 100
            change_detected = abs(change_percent) > threshold
        
        logger.info(f"Calculated hype score: {hype_score:.2f}, Change: {change_percent:.2f}%")
        return {
            "success": True,
            "averageScore": round(hype_score, 2),
            "change_detected": change_detected,
            "change_percent": round(change_percent, 2),
            "message": "Hype score calculated"
        }
    except Exception as e:
        logger.error(f"Failed to calculate hype score: {str(e)}")
        return {"success": False, "averageScore": 0.0, "change_detected": False, "change_percent": 0.0, "message": f"Failed to calculate hype score: {str(e)}"}