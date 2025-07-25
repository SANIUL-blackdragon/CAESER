import os
import requests
from datetime import datetime
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_alert(prediction, hype_data):
    """Send a Discord notification with prediction and hype score details.
    
    Args:
        prediction (dict): Prediction data (e.g., {'product': dict, 'uplift': float, 'strategy': str}).
        hype_data (dict): Hype score data (e.g., {'averageScore': float, 'change_detected': bool}).
    
    Returns:
        dict: Response with success status and message.
    """
    if not DISCORD_WEBHOOK_URL:
        logger.error("DISCORD_WEBHOOK_URL not configured")
        raise ValueError("DISCORD_WEBHOOK_URL not configured")
    
    if not isinstance(prediction, dict) or not all(key in prediction for key in ["product", "uplift", "strategy"]):
        logger.error("Invalid prediction data")
        raise ValueError("Invalid prediction data")
    if not isinstance(hype_data, dict) or "averageScore" not in hype_data:
        logger.error("Invalid hype data")
        raise ValueError("Invalid hype data")
    
    embed = {
        "title": f"New Prediction for {prediction['product'].get('name', 'Unknown Product')}",
        "description": (
            f"**Category**: {prediction['product'].get('category', 'Unknown')}\n"
            f"**Uplift**: {prediction['uplift']:.2f}%\n"
            f"**Strategy**: {prediction['strategy']}\n"
            f"**Hype Score**: {hype_data['averageScore']:.2f}"
        ),
        "color": 0x667eea,
        "footer": {"text": "CÆSER System"},
        "fields": [
            {"name": "Insights Source", "value": "Qloo Taste AI™", "inline": True},
            {"name": "Prediction Source", "value": "OpenRouter (DeepSeek)", "inline": True}
        ]
    }
    
    if hype_data.get("change_detected", False):
        embed["description"] += f"\n**Alert**: Hype score changed by {hype_data['change_percent']:.2f}%!"
        embed["color"] = 0xff0000  # Red for alerts
    
    payload = {"embeds": [embed]}
    
    try:
        logger.info(f"Sending Discord alert for {prediction['product'].get('name', 'Unknown Product')}")
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        logger.info("Discord alert sent successfully")
        return {"success": True, "message": "Discord alert sent successfully"}
    except requests.RequestException as e:
        logger.error(f"Failed to send Discord alert: {str(e)}")
        return {"success": False, "message": f"Failed to send Discord alert: {str(e)}"}