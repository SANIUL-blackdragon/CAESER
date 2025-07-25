from api.utils.logging import setup_logging
logger = setup_logging()
from fastapi import FastAPI
from .services import qloo_service, llm_service, discord_service, hype_engine
import logging
import sqlite3
import os

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

@app.get("/insights/{location}/{category}")
async def get_insights(location: str, category: str, insight_type: str = "brand"):
    """Fetch cultural insights for a location and category."""
    logger.info(f"Fetching insights for {location}/{category}/{insight_type}")
    return qloo_service.get_cultural_insights(location, category, insight_type)

@app.post("/predict/demand")
async def predict_demand(data: dict):
    """Generate demand prediction based on product and insights."""
    product = data.get("product")
    insights = data.get("insights")
    logger.info(f"Generating prediction for product: {product.get('name', 'Unknown')}")
    return llm_service.get_prediction(product, insights)

@app.post("/hype/score")
async def calculate_hype_score(data: dict):
    """Calculate hype score based on insights with change detection."""
    insights = data.get("insights")
    category = data.get("category")
    location = data.get("location")
    threshold = data.get("threshold", 20.0)
    logger.info("Calculating hype score")
    return hype_engine.calculate_hype_score(insights, category, location, threshold)

@app.post("/discord/alert")
async def send_discord_alert(data: dict):
    """Send Discord alert with prediction and hype score."""
    prediction = data.get("prediction")
    hype_data = data.get("hype_data")
    logger.info(f"Sending Discord alert for {prediction.get('product', {}).get('name', 'Unknown')}")
    return discord_service.send_alert(prediction, hype_data)

@app.get("/hype/history/{location}/{category}")
async def get_hype_history(location: str, category: str):
    """Retrieve historical hype scores for a location and category."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT score, created_at FROM hype_scores 
            WHERE category = ? AND location = ?
            ORDER BY created_at ASC
        """, (category, location))
        rows = cursor.fetchall()
        conn.close()
        return {"success": True, "data": [{"score": row[0], "timestamp": row[1]} for row in rows], "message": "History retrieved"}
    except Exception as e:
        logger.error(f"Failed to retrieve hype history: {str(e)}")
        return {"success": False, "data": [], "message": f"Failed to retrieve hype history: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check endpoint called")
    return {"status": "ok"}
logger.info('Test log message from api/main.py')