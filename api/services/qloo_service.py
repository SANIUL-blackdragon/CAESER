import os
import requests
import logging
from retrying import retry
from cachetools import TTLCache
from typing import Dict, Optional, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cache = TTLCache(maxsize=100, ttl=3600)

QLOO_API_KEY = os.getenv("QLOO_API_KEY")
BASE_URL = "https://hackathon.api.qloo.com/v2/insights"

def sanitize_input(input_str: str) -> str:
    return input_str.strip().replace(r"[^a-zA-Z0-9\s,.-]", "")

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=5000)
def get_cultural_insights(location: str, tags: List[str], insight_type: str = "brand") -> Dict:
    """Fetch cultural insights from Qloo API for a given location and tags."""
    if not QLOO_API_KEY:
        logger.error("QLOO_API_KEY not configured")
        raise ValueError("QLOO_API_KEY not configured")
    if not location or not isinstance(location, str) or not location.strip():
        logger.error("Invalid location provided")
        raise ValueError("Invalid location")
    if not tags or not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        logger.error("Invalid tags provided")
        raise ValueError("Invalid tags")
    
    location = sanitize_input(location)
    tags = [sanitize_input(tag) for tag in tags]
    
    cache_key = f"{insight_type}:{location}:{','.join(tags)}"
    if cache_key in cache:
        logger.info(f"Returning cached insights for {cache_key}")
        return cache[cache_key]
    
    headers = {
        "X-Api-Key": QLOO_API_KEY,
        "Content-Type": "application/json"
    }
    
    filter_tags = ",".join([f"urn:tag:keyword:brand:{tag.lower()}" for tag in tags])
    params = {}
    if insight_type == "brand":
        params = {
            "filter.type": "urn:entity:brand",
            "signal.location.query": location if location != "global" else None,
            "filter.tags": filter_tags
        }
    elif insight_type == "demographics":
        params = {
            "filter.type": "urn:demographics",
            "signal.location.query": location if location != "global" else None,
            "signal.interests.tags": filter_tags
        }
    elif insight_type == "heatmap":
        params = {
            "filter.type": "urn:heatmap",
            "filter.location.query": location if location != "global" else None,
            "signal.interests.tags": filter_tags
        }
    else:
        logger.error(f"Unsupported insight type: {insight_type}")
        raise ValueError(f"Unsupported insight type: {insight_type}")
    
    try:
        logger.info(f"Fetching {insight_type} insights for {location} with tags {tags}")
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get("success"):
            logger.error(f"Invalid API response: {data.get('message', 'Unknown error')}")
            raise ValueError(f"Invalid API response: {data.get('message', 'Unknown error')}")
        
        result = {"success": True, "data": data["results"], "message": f"{insight_type.capitalize()} insights retrieved successfully"}
        cache[cache_key] = result
        logger.info(f"Cached insights for {cache_key}")
        return result
    except requests.RequestException as e:
        logger.error(f"Qloo API request failed: {str(e)}")
        return {"success": False, "data": None, "message": f"Qloo API request failed: {str(e)}"}