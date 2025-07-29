import sqlite3
import os
from datetime import datetime, timedelta
import logging
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def predict_trend(product_name: str, tags: str) -> dict:
    """
    Predict the time period of a trend based on Google Trends and social data.
    
    Args:
        product_name (str): Name of the product.
        tags (str): Comma-separated tags related to the product.
    
    Returns:
        dict: Prediction result with peak days, date, and confidence.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Fetch relevant trend data (e.g., from social_data table)
        tags_list = [tag.strip() for tag in tags.split(",")]
        query = """
            SELECT likes, timestamp FROM social_data 
            WHERE source='google_trends' AND (text LIKE ? OR text IN ({}))
            ORDER BY timestamp ASC
        """.format(",".join(["?"] * len(tags_list)))
        params = [f"%{product_name}%"] + tags_list
        cursor.execute(query, params)
        data = cursor.fetchall()
        
        if not data:
            logger.warning(f"No trend data found for {product_name} with tags {tags}")
            return {"success": False, "message": "No trend data available"}
        
        # Extract time series data
        likes = [row[0] for row in data]
        timestamps = [datetime.fromisoformat(row[1]) for row in data]
        
        # Simple time series prediction using Exponential Smoothing
        if len(likes) < 3:
            logger.warning("Insufficient data points for prediction")
            return {"success": False, "message": "Insufficient data for prediction"}
        
        model = ExponentialSmoothing(likes, trend="add", seasonal=None)
        fit = model.fit()
        forecast = fit.forecast(90)  # Predict next 90 days
        peak_idx = np.argmax(forecast)
        peak_days = peak_idx + 1  # Days until peak
        peak_date = (timestamps[-1] + timedelta(days=peak_days)).strftime("%Y-%m-%d")
        confidence = min(0.95, 1.0 - fit.sse / sum(l**2 for l in likes))  # Simple confidence metric
        
        # Store the prediction
        cursor.execute("""
            INSERT INTO trend_predictions (product_name, tags, predicted_peak_days, predicted_peak_date, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product_name, tags, float(peak_days), peak_date, confidence, datetime.now().isoformat()))
        conn.commit()
        
        result = {
            "success": True,
            "predicted_peak_days": int(peak_days),
            "predicted_peak_date": peak_date,
            "confidence": confidence
        }
        logger.info(f"Trend predicted for {product_name}: Peak in {peak_days} days on {peak_date}")
        return result
    
    except Exception as e:
        logger.error(f"Trend prediction failed: {str(e)}")
        return {"success": False, "message": f"Prediction failed: {str(e)}"}
    
    finally:
        conn.close()

if __name__ == "__main__":
    # For testing purposes
    result = predict_trend("Wireless Headphones", "electronics, audio")
    print(result)