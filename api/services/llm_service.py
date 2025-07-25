import os
from openai import OpenAI
from retrying import retry
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://caeser.example.com"
SITE_NAME = "CÆSER"

def sanitize_input(input_data):
    """Remove potentially harmful characters from input to prevent injection."""
    if isinstance(input_data, str):
        return input_data.strip().replace(r'[^\w\s,.-]', '')
    return input_data

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=5000)
def get_prediction(product, insights):
    """Generate demand prediction and marketing strategy using OpenRouter API.
    
    Args:
        product (dict): Product details (e.g., {'name': str, 'category': str, 'description': str}).
        insights (dict): Cultural insights from Qloo API.
    
    Returns:
        dict: Response with success status, data (uplift and strategy), and message.
    
    Raises:
        ValueError: If API key or inputs are invalid.
        Exception: If API call fails.
    """
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not configured")
        raise ValueError("OPENROUTER_API_KEY not configured")
    
    if not isinstance(product, dict) or not all(key in product for key in ["name", "category", "description"]):
        logger.error("Invalid product data: must include name, category, description")
        raise ValueError("Invalid product data: must include name, category, description")
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    
    # Sanitize inputs
    product_name = sanitize_input(product["name"])
    product_category = sanitize_input(product["category"])
    product_description = sanitize_input(product["description"])
    
    # Initialize OpenRouter client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    # Construct prompt
    prompt = f"""
    Analyze the following product and cultural insights to predict demand uplift and suggest a marketing strategy.
    Product: {product_name} ({product_category})
    Description: {product_description}
    Cultural Insights: {insights['data']}
    Provide a response in JSON format with 'uplift' (percentage, float) and 'strategy' (string).
    """
    
    try:
        logger.info(f"Generating prediction for {product_name}")
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
              model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        result = completion.choices[0].message.content.strip()
        import json
        parsed_result = json.loads(result)
        if not all(key in parsed_result for key in ["uplift", "strategy"]):
            logger.error("Invalid LLM response format")
            raise ValueError("Invalid LLM response format")
        logger.info(f"Prediction generated successfully for {product_name}")
        return {"success": True, "data": parsed_result, "message": "Prediction generated successfully"}
    except Exception as e:
        logger.error(f"LLM request failed: {str(e)}")
        return {"success": False, "data": None, "message": f"LLM request failed: {str(e)}"}