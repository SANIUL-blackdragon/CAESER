from api.utils.logging import setup_logging
logger = setup_logging()
from fastapi import FastAPI
from .services import qloo_service, llm_service, discord_service, hype_engine
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

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
    """Calculate hype score based on insights."""
    insights = data.get("insights")
    logger.info("Calculating hype score")
    return hype_engine.calculate_hype_score(insights)

@app.post("/discord/alert")
async def send_discord_alert(data: dict):
    """Send Discord alert with prediction and hype score."""
    prediction = data.get("prediction")
    hype_data = data.get("hype_data")
    logger.info(f"Sending Discord alert for {prediction.get('product', {}).get('name', 'Unknown')}")
    return discord_service.send_alert(prediction, hype_data)
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check endpoint called")
    return {"status": "ok"}
logger.info('Test log message from api/main.py')