from fastapi import FastAPI
from .services import qloo_service, llm_service, discord_service, hype_engine, integrations_service, data_quality_service
from .services.predict_trend import predict_trend
import logging
import sqlite3
import os
import pytz
from datetime import datetime
import subprocess
import random
import time
from pydantic import BaseModel
from typing import Optional
import math
import json
import pandas as pd
from datetime import timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db").strip('\'"')
if not isinstance(DB_PATH, str):
    raise ValueError("DB_PATH must be a string")

class LogMessageIn(BaseModel):
    new_message: str

class CompetitorIn(BaseModel):
    name: str
    hype_score: float
class FeedbackIn(BaseModel):
    user_id: str
    product_name: str
    category: str
    feedback_text: str
    sentiment_weight: float = 1.0

class RetrainOut(BaseModel):
    success: bool
    message: str
    new_weights: dict

class TrendPredictionInput(BaseModel):
    product_name: str
    tags: str
    time_period: str  # Optional, e.g., "90 days" (not used in initial version)

class AnalyzeInput(BaseModel):
    product_name: str
    description: str
    tags: str
    target_area: Optional[str] = None
    locations: Optional[str] = None
    gender: Optional[str] = None

class CategoryIn(BaseModel):
    category_name: str
    keywords: str   # comma-separated

@app.on_event("startup")
async def startup_event():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            timestamp TEXT,
            details TEXT
        )
    """)
    
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
        CREATE TABLE IF NOT EXISTS trend_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            tags TEXT,
            predicted_peak_days REAL,
            predicted_peak_date TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)
    
    utc_time = datetime.now(pytz.utc).isoformat()
    cursor.execute("""
        INSERT INTO system_events (event_type, timestamp)
        VALUES (?, ?)
    """, ("startup", utc_time))
    
    conn.commit()
    conn.close()
    logger.info(f"System started at {utc_time}")

@app.post("/admin/log_message")
def set_log_message(body: LogMessageIn):
    os.environ["STARTUP_MESSAGE"] = body.new_message
    return {"success": True, "message": "Next restart will use the new message"}

@app.get("/competitors")
async def competitors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT name, hype_score FROM competitors")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: {"hype": row[1]} for row in rows}

@app.post("/competitors/add")
async def add_competitor(body: CompetitorIn):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO competitors (name, hype_score) VALUES (?, ?)",
        (body.name, body.hype_score)
    )
    cursor.execute(
        "UPDATE competitors SET hype_score = ? WHERE name = ?",
        (body.hype_score, body.name)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Competitor {body.name} saved/updated"}

@app.post("/categories")
def add_or_update_category(body: CategoryIn):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO categories (category_name, keywords)
        VALUES (?, ?)
        ON CONFLICT(category_name) DO UPDATE SET keywords=excluded.keywords
    """, (body.category_name, body.keywords))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Category '{body.category_name}' saved"}

@app.get("/categories")
def list_categories():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT category_name, keywords FROM categories")
    rows = cur.fetchall()
    conn.close()
    return {"success": True, "data": {r[0]: r[1].split(",") for r in rows}}

# ---------- dynamic insight types ----------
@app.get("/insight_types")
async def get_insight_types():
    """Return available insight types from insight_types table."""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT type_name FROM insight_types ORDER BY type_name")
    types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return types

@app.post("/analyze")
async def analyze(input: AnalyzeInput):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/analyze", input.json(), datetime.now(pytz.utc).isoformat()))
    conn.commit()
    conn.close()
    
    try:
        keywords = [kw.strip() for kw in input.tags.split(",")]
        locations = [loc.strip() for loc in input.locations.split(",")] if input.locations else []
        gender = input.gender
        
        # Trigger data collection with target set to product_name
        sources = "reddit,tiktok,instagram,imdb,ebay"  # default; could come from request body
        cmd = [
            "scrapy", "crawl", "social_media",
            "-a", f"target={input.product_name}",
            "-a", f"sources={sources}",      # ⬅️ NEW
            "-a", f"keywords={','.join(keywords)}"
        ]
        if locations:
            cmd.extend(["-a", f"locations={','.join(locations)}"])
        if gender:
            cmd.extend(["-a", f"gender={gender}"])
        
        logger.info(f"Running scraping command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Scraping failed: {result.stderr}")
            return {"success": False, "hype_score": 0.0, "trend_prediction": None, "message": f"Scraping failed: {result.stderr}"}
        
        logger.info(f"Scraping completed: {result.stdout}")
        # Use configured mock score range or real calculation if available
        min_score = float(os.getenv("MOCK_HYPE_MIN", "0"))
        max_score = float(os.getenv("MOCK_HYPE_MAX", "100"))
        # Real hype score calculated from scraped data / insights
        hype_score = hype_engine.calculate_hype_score(
            insights if insights else {},
            ','.join(keywords),
            location or 'global',
            20.0
        ).get("averageScore", 0.0)
        logger.info(f"Calculated hype score: {hype_score}")
        # Log the hype score
        
        # Generate trend prediction
        trend_result = predict_trend(input.product_name, input.tags)
        
        response = {
            "success": True,
            "hype_score": hype_score,
            "trend_prediction": trend_result if trend_result["success"] else None,
            "message": "Analysis completed successfully"
        }
        return response
    
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return {
            "success": False,
            "hype_score": 0.0,
            "trend_prediction": None,
            "message": f"Analysis failed: {str(e)}"
        }
    
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/analyze", dur, datetime.now(pytz.utc).isoformat())
        ).connection.commit()

@app.get("/insights/{location}")
async def get_insights(location: str, tags: str, insight_type: str = "brand"):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        (f"/insights/{location}", json.dumps({"tags": tags, "insight_type": insight_type}), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        logger.info(f"Fetching insights for {location} with tags {tags_list}")
        return qloo_service.get_cultural_insights(location, tags_list, insight_type)
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            (f"/insights/{location}", dur, datetime.now(pytz.utc).isoformat())
        ).connection.commit()

@app.get("/llm_data_quality")
async def get_llm_data_quality():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/llm_data_quality", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        logger.info("Fetching LLM data quality metrics")
        return llm_service.get_llm_data_quality()
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/llm_data_quality", dur, datetime.now(pytz.utc).isoformat())
        ).connection.commit()

@app.get("/data_quality")
async def get_data_quality():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/data_quality", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        logger.info("Fetching general data quality metrics")
        return data_quality_service.check_data_quality()
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/data_quality", dur, datetime.now(pytz.utc).isoformat())
        ).connection.commit()

@app.post("/predict/demand")
async def predict_demand(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary")
    
    product = data.get("product", {})
    insights = data.get("insights", {})
    hype_score = data.get("hype_score", 0.0)
    
    if not isinstance(product, dict) or not isinstance(insights, dict):
        return {"success": False, "message": "Invalid input format"}
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/predict/demand", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        product = data.get("product")
        insights = data.get("insights")
        hype_score = data.get("hype_score", 0.0)
        logger.info(f"Generating prediction for product: {product.get('name', 'Unknown')}")
        prediction = llm_service.get_prediction(
            product or {},
            insights or {},
            float(hype_score)
        )
        
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
            """, (product["name"], ','.join(product["tags"]), predicted_uplift, confidence, timestamp))
            conn.commit()
            conn.close()
            logger.info(f"Saved prediction for {product['name']} to database")
        
        return prediction
    finally:
        dur = (time.time() - start) * 1000
        conn = sqlite3.connect(str(DB_PATH))
        try:
            conn.execute(
                "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
                ("/predict/demand", dur, datetime.now(pytz.utc).isoformat())
            )
            conn.commit()
        finally:
            conn.close()

@app.post("/hype/score")
async def calculate_hype_score(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary")
    
    insights = data.get("insights", {}) or {}
    tags = str(data.get("category", ""))
    location = str(data.get("location", ""))
    threshold = float(data.get("threshold", 20.0))
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/hype/score", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        insights = data.get("insights")
        tags = data.get("category")  # Assuming tags are passed as category for compatibility
        location = data.get("location")
        threshold = data.get("threshold", 20.0)
        logger.info("Calculating hype score")
        return hype_engine.calculate_hype_score(
            insights if isinstance(insights, dict) else {},
            tags,
            location,
            threshold
        )
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/hype/score", dur, datetime.now(pytz.utc).isoformat())
        ).connection.commit()

@app.post("/discord/alert")
async def send_discord_alert(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/discord/alert", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        prediction = data.get("prediction")
        hype_data = data.get("hype_data")
        product_name = "Unknown"
        if prediction and isinstance(prediction, dict):
            product = prediction.get('product', {})
            if isinstance(product, dict):
                product_name = product.get('name', 'Unknown')
        logger.info(f"Sending Discord alert for {product_name}")
        return discord_service.send_alert(prediction, hype_data)
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/discord/alert", dur, datetime.now(pytz.utc).isoformat())
        ).connection.commit()

@app.post("/integrations/send")
async def send_integrations(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/integrations/send", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        prediction = data.get("prediction")
        hype_data = data.get("hype_data")
        logger.info(f"Sending data to integrations for {prediction.get('product', {}).get('name', 'Unknown')}")
        return integrations_service.send_integrations(prediction, hype_data)
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/integrations/send", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/hype/history/{location}/{category}")
async def get_hype_history(location: str, category: str):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        (f"/hype/history/{location}/{category}", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
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
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            (f"/hype/history/{location}/{category}", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.post("/submit_outcome")
async def submit_outcome(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/submit_outcome", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        prediction_id = data.get("prediction_id")
        actual_uplift = data.get("actual_uplift")

        if not prediction_id or not isinstance(prediction_id, int) or prediction_id <= 0:
            return {"success": False, "message": "Invalid prediction_id. It must be a positive integer."}
        
        if actual_uplift is None or not isinstance(actual_uplift, (int, float)):
            return {"success": False, "message": "Invalid actual_uplift. It must be a number."}

        timestamp = datetime.now(pytz.utc).isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM predictions WHERE id = ?", (prediction_id,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return {"success": False, "message": f"No prediction found with ID {prediction_id}"}

        cursor.execute("""
            INSERT INTO outcomes (prediction_id, actual_uplift, timestamp)
            VALUES (?, ?, ?)
        """, (prediction_id, actual_uplift, timestamp))
        conn.commit()
        conn.close()
        logger.info(f"Submitted outcome for prediction ID {prediction_id}")
        return {"success": True, "message": "Outcome submitted successfully"}
    except Exception as e:
        logger.error(f"Failed to submit outcome: {str(e)}")
        return {"success": False, "message": f"Failed to submit outcome: {str(e)}"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/submit_outcome", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/calculate_loss")
async def calculate_loss(threshold: float = 80.0):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/calculate_loss", json.dumps({"threshold": threshold}), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
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
            predicted_class = 1 if row[1] >= threshold else 0
            actual_class = 1 if row[3] >= threshold else 0
            p_i = row[2] if predicted_class == 1 else 1 - row[2]
            
            if actual_class == 1:
                loss = -math.log(p_i) if p_i > 0 else float('inf')
            else:
                loss = -math.log(1 - p_i) if p_i < 1 else float('inf')
            losses.append(loss)
        
        average_loss = sum(losses) / len(losses)
        logger.info(f"Calculated average loss: {average_loss:.4f}")
        return {"success": True, "average_loss": average_loss, "message": "Loss calculated successfully"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/calculate_loss", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.post("/feedback")
async def feedback_endpoint(body: FeedbackIn):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO feedback_log
           (user_id, product_name, category, feedback_text, sentiment_weight, timestamp)
           VALUES (?,?,?,?,?,?)""",
        (body.user_id, body.product_name, body.category,
         body.feedback_text, body.sentiment_weight,
         datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    await retrain_endpoint()
    return {"success": True, "message": "Feedback stored & model retrained"}

@app.post("/retrain")
async def retrain_endpoint():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/retrain", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.sentiment, o.actual_uplift
            FROM hype_scores h
            JOIN outcomes o ON o.prediction_id = h.id
            ORDER BY h.created_at DESC LIMIT 100
        """)
        rows = cursor.fetchall()
        if not rows:
            conn.close()
            return {"success": False, "message": "Need ≥1 outcome to retrain"}
        sentiments = [r[0] for r in rows]
        actuals = [r[1] for r in rows]
        new_weight = sum(actuals) / (sum(sentiments) + 1e-9)
        cursor.execute("INSERT OR REPLACE INTO model_weights(key,value) VALUES('sentiment_weight',?)", (new_weight,))
        conn.commit()
        conn.close()
        return RetrainOut(success=True, message="Weights updated", new_weights={"sentiment_weight": new_weight})
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/retrain", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/runtime_estimates")
async def runtime_estimates():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/runtime_estimates", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(duration_ms) FROM api_calls ORDER BY id DESC LIMIT 50")
        avg = cursor.fetchone()[0] or 0
        conn.close()
        return {"average_duration_ms": avg, "estimate": f"≈ {avg/1000:.1f}s"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/runtime_estimates", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/error_logs")
async def error_logs(limit: int = 50):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/error_logs", json.dumps({"limit": limit}), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM error_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        logs = cursor.fetchall()
        conn.close()
        return {"logs": [dict(row) for row in logs]}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/error_logs", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/health")
async def health_check():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/health", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        logger.info("Health check endpoint called")
        return {"status": "ok"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/health", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/export_model")
async def export_model():
    return {"script": "def score(hype, sent): return hype*sentiment_weight + sent*popularity_weight"}

@app.post("/custom_score")
async def custom_score(py_code: str):
    exec(py_code, globals())
    return {"success": True, "message": "Custom scorer uploaded"}

@app.get("/backtest")
async def backtest():
    return {"mock_2023_campaign": {"predicted": 15, "actual": 12, "error": 3}}

# New endpoint for trend duration prediction
@app.post("/predict/trend_duration")
async def predict_trend_duration(input: TrendPredictionInput):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
                 ("/predict/trend_duration", json.dumps(input.dict()), datetime.now(pytz.utc).isoformat()))
    conn.commit()
    
    try:
        # Fetch historical trend data from social_data (Google Trends)
        conn = sqlite3.connect(DB_PATH)
        query = """
            SELECT timestamp, likes AS interest 
            FROM social_data 
            WHERE source='google_trends' AND text IN ({}) 
            ORDER BY timestamp
        """.format(','.join(['?' for _ in input.tags.split(',')]))
        df = pd.read_sql_query(query, conn, params=input.tags.split(','))
        conn.close()
        
        if df.empty:
            logger.warning(f"No historical trend data found for tags: {input.tags}")
            return {
                "success": False,
                "message": "Insufficient historical trend data",
                "predicted_duration_days": 0,
                "predicted_peak_time": None,
                "confidence": 0.0
            }
        
        # Convert timestamp to datetime and sort
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Aggregate interest by day (assuming multiple entries per day)
        daily_df = df.groupby(df['timestamp'].dt.date)['interest'].mean().reset_index()
        daily_df['timestamp'] = pd.to_datetime(daily_df['timestamp'])
        
        # Fit exponential smoothing model
        model = ExponentialSmoothing(
            daily_df['interest'],
            trend='add',
            seasonal=None,
            damped_trend=True
        )
        fit = model.fit()
        
        # Forecast future trend (e.g., 90 days)
        forecast_steps = 90
        forecast = fit.forecast(forecast_steps)
        
        # Calculate trend duration and peak
        peak_idx = np.argmax(forecast)
        peak_time = daily_df['timestamp'].iloc[-1] + timedelta(days=peak_idx + 1)
        duration_days = forecast_steps  # Simplistic assumption: duration until forecast end
        confidence = 0.85  # Mock confidence; could be based on model fit
        
        # Store prediction
        timestamp = datetime.now(pytz.utc).isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trend_predictions (product_name, tags, predicted_duration_days, predicted_peak_time, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (input.product_name, input.tags, float(duration_days), peak_time.isoformat(), confidence, timestamp))
        conn.commit()
        conn.close()
        
        logger.info(f"Trend prediction saved for {input.product_name}: Duration={duration_days} days, Peak={peak_time}")
        
        return {
            "success": True,
            "predicted_duration_days": float(duration_days),
            "predicted_peak_time": peak_time.isoformat(),
            "confidence": confidence,
            "message": "Trend duration predicted successfully"
        }
    
    except Exception as e:
        logger.error(f"Trend prediction failed: {str(e)}")
        return {
            "success": False,
            "predicted_duration_days": 0,
            "predicted_peak_time": None,
            "confidence": 0.0,
            "message": f"Prediction failed: {str(e)}"
        }
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/predict/trend_duration", dur, datetime.now(pytz.utc).isoformat())
        ).connection.commit()

@app.get("/competitors")
async def competitors():
    return {"nike": {"hype": 78}, "adidas": {"hype": 65}}

logger.info(os.getenv("STARTUP_MESSAGE", "API initialized successfully"))