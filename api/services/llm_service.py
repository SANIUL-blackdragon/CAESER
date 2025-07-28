import os
import json
import time
import sqlite3
import logging
from openai import OpenAI
from typing import Dict

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "http://localhost:8000"
SITE_NAME = "CAESER"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sanitize_input(input_str: str) -> str:
    return input_str.strip().replace(r"[^a-zA-Z0-9\s,.-]", "")

def log_llm_data_quality(metric: str, value: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO llm_data_quality (metric, value, timestamp)
        VALUES (?, ?, ?)
    """, (metric, value, time.time()))
    conn.commit()
    conn.close()

def get_prediction(product: Dict, insights: Dict, hype_score: float) -> Dict:
    """Generate demand prediction and marketing strategy using LLM."""
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not configured")
        raise ValueError("OPENROUTER_API_KEY not configured")
    
    if not isinstance(product, dict) or not all(key in product for key in ["name", "tags", "description"]):
        logger.error("Invalid product data: must include name, tags, description")
        raise ValueError("Invalid product data")
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    
    product_name = sanitize_input(product["name"])
    product_tags = ", ".join([sanitize_input(tag) for tag in product["tags"]])
    product_description = sanitize_input(product["description"])
    location = sanitize_input(product.get("location", "Global"))
    age_range = sanitize_input(product.get("age_range", "All"))
    gender = sanitize_input(product.get("gender", "All"))
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    prompt = f"""
    Analyze the following product and cultural insights to predict demand uplift and suggest a marketing strategy.
    Product: {product_name}
    Tags: {product_tags}
    Description: {product_description}
    Target Market: {location}, Age: {age_range}, Gender: {gender}
    Cultural Insights: {insights['data']}
    Hype Score: {hype_score}
    Provide a response in JSON format with 'uplift' (percentage, float), 'strategy' (string), 'confidence' (float between 0 and 1), and 'trend' (list of dicts with 'time' and 'demand').
    """
    
    try:
        start_time = time.time()
        logger.info(f"Generating prediction for {product_name}")
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )
        result = completion.choices[0].message.content.strip()
        parsed_result = json.loads(result)
        if not all(key in parsed_result for key in ["uplift", "strategy", "confidence", "trend"]):
            logger.error("Invalid LLM response format")
            raise ValueError("Invalid LLM response format")
        
        confidence = parsed_result.get("confidence", 0.0)
        response_time = time.time() - start_time
        log_llm_data_quality("confidence", confidence)
        log_llm_data_quality("response_time", response_time)
        
        logger.info(f"Prediction generated successfully for {product_name}")
        parsed_result["cpc"] = 1.0   # TikTok mock CPC ($1)
        parsed_result["cpm"] = 5.0   # TikTok mock CPM ($5)
        return {"success": True, "data": parsed_result, "message": "Prediction generated successfully"}
    except Exception as e:
        log_llm_data_quality("errors", 1.0)
        logger.error(f"LLM request failed: {str(e)}")
        return {"success": False, "data": None, "message": f"LLM request failed: {str(e)}"}

def get_llm_data_quality():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT metric, AVG(value) as avg_value, COUNT(*) as count
        FROM llm_data_quality
        GROUP BY metric
    """)
    rows = cursor.fetchall()
    conn.close()
    metrics = {row[0]: {"avg_value": row[1], "count": row[2]} for row in rows}
    return {
        "success": True,
        "data": metrics,
        "message": "LLM data quality metrics retrieved"
    }