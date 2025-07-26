import os
import sqlite3
from openai import OpenAI
from retrying import retry
import logging
import json
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://caeser.example.com"
SITE_NAME = "CÆSER"
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def sanitize_input(input_data):
    if isinstance(input_data, str):
        return input_data.strip().replace(r'[^\w\s,.-]', '')
    return input_data

def log_llm_data_quality(metric: str, value: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO llm_data_quality (metric, value, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    """, (metric, value))
    conn.commit()
    conn.close()
    logger.info(f"Logged LLM data quality: {metric} = {value}")

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=5000)
def get_prediction(product, insights):
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not configured")
        raise ValueError("OPENROUTER_API_KEY not configured")
    
    if not isinstance(product, dict) or not all(key in product for key in ["name", "category", "description"]):
        logger.error("Invalid product data: must include name, category, description")
        raise ValueError("Invalid product data")
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    
    product_name = sanitize_input(product["name"])
    product_category = sanitize_input(product["category"])
    product_description = sanitize_input(product["description"])
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    prompt = f"""
    Analyze the following product and cultural insights to predict demand uplift and suggest a marketing strategy.
    Product: {product_name} ({product_category})
    Description: {product_description}
    Cultural Insights: {insights['data']}
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
        
        # Log data quality metrics
        confidence = parsed_result.get("confidence", 0.0)
        response_time = time.time() - start_time
        log_llm_data_quality("confidence", confidence)
        log_llm_data_quality("response_time", response_time)
        
        logger.info(f"Prediction generated successfully for {product_name}")
        parsed_result["cpc"] = 1.0   # TikTok mock CPC ($1)
        parsed_result["cpm"] = 5.0   # TikTok mock CPM ($5)
        return {"success": True, "data": parsed_result, "message": "Prediction generated successfully"}
    except Exception as e:
        log_llm_data_quality("errors", 1.0)  # Log error occurrence
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