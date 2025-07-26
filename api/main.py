from api.utils.logging import setup_logging
logger = setup_logging()
from fastapi import FastAPI
from .services import qloo_service, llm_service, discord_service, hype_engine, integrations_service, data_quality_service
import logging
import sqlite3
import os
import pytz
from datetime import datetime
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

# Global variable for historical forecasts
historical_forecasts = []

@app.on_event("startup")
async def startup_event():
    # Create system_events table if it doesn't exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create system_events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            timestamp TEXT,
            details TEXT
        )
    """)
    
    # Create predictions and outcomes tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            category TEXT,
            predicted_uplift REAL,
            confidence REAL,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outcomes (
            prediction_id INTEGER,
            actual_uplift REAL,
            timestamp TEXT,
            FOREIGN KEY(prediction_id) REFERENCES predictions(id)
        )
    """)
    
    # Log startup time in UTC
    utc_time = datetime.now(pytz.utc).isoformat()
    cursor.execute("""
        INSERT INTO system_events (event_type, timestamp)
        VALUES (?, ?)
    """, ("startup", utc_time))
    
    # Load historical forecasts
    cursor.execute("""
        SELECT score, timestamp FROM hype_scores 
        ORDER BY timestamp DESC LIMIT 100
    """)
    global historical_forecasts
    historical_forecasts = cursor.fetchall()
    
    conn.commit()
    conn.close()
    logger.info(f"System started at {utc_time}, loaded {len(historical_forecasts)} historical forecasts")

@app.get("/insights/{location}/{category}")
async def get_insights(location: str, category: str, insight_type: str = "brand"):
    logger.info(f"Fetching insights for {location}/{category}/{insight_type}")
    return qloo_service.get_cultural_insights(location, category, insight_type)

@app.get("/llm_data_quality")
async def get_llm_data_quality():
    logger.info("Fetching LLM data quality metrics")
    return llm_service.get_llm_data_quality()

@app.get("/data_quality")
async def get_data_quality():
    logger.info("Fetching general data quality metrics")
    return data_quality_service.check_data_quality()

@app.post("/predict/demand")
async def predict_demand(data: dict):
    product = data.get("product")
    insights = data.get("insights")
    logger.info(f"Generating prediction for product: {product.get('name', 'Unknown')}")
    prediction = llm_service.get_prediction(product, insights)
    
    # Save prediction to database
    if prediction and prediction.get("success"):
        prediction_data = prediction["data"]
        predicted_uplift = prediction_data.get("uplift", 0.0)
        confidence = prediction_data.get("confidence", 0.5)
        timestamp = datetime.now(pytz.utc).isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (product_name, category, predicted_uplift, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (product["name"], product["category"], predicted_uplift, confidence, timestamp))
        conn.commit()
        conn.close()
        logger.info(f"Saved prediction for {product['name']} to database")
    
    return prediction

@app.post("/hype/score")
async def calculate_hype_score(data: dict):
    insights = data.get("insights")
    category = data.get("category")
    location = data.get("location")
    threshold = data.get("threshold", 20.0)
    logger.info("Calculating hype score")
    return hype_engine.calculate_hype_score(insights, category, location, threshold)

@app.post("/discord/alert")
async def send_discord_alert(data: dict):
    prediction = data.get("prediction")
    hype_data = data.get("hype_data")
    logger.info(f"Sending Discord alert for {prediction.get('product', {}).get('name', 'Unknown')}")
    return discord_service.send_alert(prediction, hype_data)

@app.post("/integrations/send")
async def send_integrations(data: dict):
    prediction = data.get("prediction")
    hype_data = data.get("hype_data")
    logger.info(f"Sending data to integrations for {prediction.get('product', {}).get('name', 'Unknown')}")
    return integrations_service.send_integrations(prediction, hype_data)

@app.get("/hype/history/{location}/{category}")
async def get_hype_history(location: str, category: str):
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

@app.post("/submit_outcome")
async def submit_outcome(data: dict):
    prediction_id = data.get("prediction_id")
    actual_uplift = data.get("actual_uplift")
    if not prediction_id or actual_uplift is None:
        return {"success": False, "message": "Missing prediction_id or actual_uplift"}
    
    timestamp = datetime.now(pytz.utc).isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO outcomes (prediction_id, actual_uplift, timestamp)
        VALUES (?, ?, ?)
    """, (prediction_id, actual_uplift, timestamp))
    conn.commit()
    conn.close()
    logger.info(f"Submitted outcome for prediction ID {prediction_id}")
    return {"success": True, "message": "Outcome submitted successfully"}

@app.get("/calculate_loss")
async def calculate_loss(threshold: float = 80.0):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.predicted_uplift, p.confidence, o.actual_uplift
            FROM predictions p
            JOIN outcomes o ON p.id = o.prediction_id
            ORDER BY p.timestamp DESC LIMIT 10
        """)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return {"success": False, "message": "No predictions with outcomes available"}
        
        losses = []
        for row in rows:
            predicted_class = 1 if row[1] >= threshold else 0  # predicted_uplift >= threshold%
            actual_class = 1 if row[3] >= threshold else 0     # actual_uplift >= threshold%
            p_i = row[2] if predicted_class == 1 else 1 - row[2]  # confidence for predicted class
            
            # Calculate cross-entropy loss
            if actual_class == 1:
                loss = -math.log(p_i) if p_i > 0 else float('inf')
            else:
                loss = -math.log(1 - p_i) if p_i < 1 else float('inf')
            losses.append(loss)
        
        average_loss = sum(losses) / len(losses)
        logger.info(f"Calculated average loss: {average_loss:.4f}")
        return {"success": True, "average_loss": average_loss, "message": "Loss calculated successfully"}
    
    except Exception as e:
        logger.error(f"Failed to calculate loss: {str(e)}")
        return {"success": False, "message": f"Failed to calculate loss: {str(e)}"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

logger.info('API initialized successfully')