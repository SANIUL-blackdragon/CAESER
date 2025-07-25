```python
import random
from typing import Dict
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

def calculate_hype_score(insights: Dict) -> Dict:
    """Calculate a hype score based on cultural insights with simulated consumer behavior.
    
    Args:
        insights (dict): Cultural insights from Qloo API.
    
    Returns:
        Dict: Hype score (0-100) with success status and message.
    
    Raises:
        ValueError: If insights data is invalid.
    """
    validate_insights(insights)
    
    try:
        # Extract popularity from Qloo API entities
        entities = insights["data"].get("entities", [])
        if not entities:
            logger.warning("No entities found in insights data, using default popularity")
            popularity = 0.5
        else:
            popularity = sum(entity["properties"].get("popularity", 0.5) for entity in entities) / len(entities)
        
        # Simulate trend factor (could be enhanced with bias.trends from Qloo API)
        trend_factor = insights["data"].get("trend", 1.0)
        
        # Calculate base score
        base_score = popularity * 100 * trend_factor
        simulation_noise = random.uniform(-10, 10)  # Add randomness for realism
        
        # Normalize to 0-100
        hype_score = max(0.0, min(100.0, base_score + simulation_noise))
        
        logger.info(f"Calculated hype score: {hype_score:.2f}")
        return {"success": True, "averageScore": round(hype_score, 2), "message": "Hype score calculated"}
    except Exception as e:
        logger.error(f"Failed to calculate hype score: {str(e)}")
        return {"success": False, "averageScore": 0.0, "message": f"Failed to calculate hype score: {str(e)}"}
```