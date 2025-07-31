import sqlite3
import os
from datetime import datetime, timedelta
import logging
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Optional Prophet import (graceful fallback)
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
def predict_trend(product_name: str, tags: str) -> dict:
    """
    Predict trend peak using Holt-Winters or Prophet (if available and data is large).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure index exists
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_trend_lookup ON social_data(source, text)"
        )

        tags_list = [tag.strip() for tag in tags.split(",")]
        placeholders = ",".join(["?"] * len(tags_list))
        query = f"""
            SELECT likes, timestamp FROM social_data
            WHERE source='google_trends' AND (text LIKE ? OR text IN ({placeholders}))
            ORDER BY timestamp ASC
        """
        params = [f"%{product_name}%"] + tags_list
        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            logger.warning("No trend data for %s (%s)", product_name, tags)
            return {"success": False, "message": "No trend data"}

        likes = np.array([r[0] for r in rows], dtype=float)
        timestamps = [datetime.fromisoformat(r[1]) for r in rows]

        if len(likes) < 3:
            logger.warning("Insufficient data points")
            return {"success": False, "message": "Insufficient data"}

        # --- Model choice ---
        if HAS_PROPHET and len(likes) > 30:
            # Prophet for longer series
            df = pd.DataFrame({
                "ds": timestamps,
                "y": likes
            })
            m = Prophet()
            m.fit(df)
            future = m.make_future_dataframe(periods=90)
            forecast = m.predict(future)
            peak_row = forecast.loc[forecast["yhat"].idxmax()]
            peak_date = peak_row["ds"].strftime("%Y-%m-%d")
            peak_days = (peak_row["ds"] - timestamps[-1]).days
            confidence = 0.9  # Prophet gives intervals; simplified here
        else:
            # Holt-Winters (faster for short series)
            model = ExponentialSmoothing(likes, trend="add", seasonal=None)
            fit = model.fit()
            fcast = fit.forecast(90)
            peak_idx = int(np.argmax(fcast))
            peak_days = peak_idx + 1
            peak_date = (timestamps[-1] + timedelta(days=peak_days)).strftime("%Y-%m-%d")
            confidence = min(0.95, 1.0 - fit.sse / np.sum(likes ** 2))

        cursor.execute("""
            INSERT INTO trend_predictions
            (product_name, tags, predicted_peak_days, predicted_peak_date, confidence, timestamp)
            VALUES (?,?,?,?,?,?)
        """, (product_name, tags, float(peak_days), peak_date, confidence,
              datetime.now().isoformat()))
        conn.commit()

        logger.info("Trend for %s: peak in %d days on %s (%.2f conf)",
                    product_name, peak_days, peak_date, confidence)
        return {
            "success": True,
            "predicted_peak_days": int(peak_days),
            "predicted_peak_date": peak_date,
            "confidence": confidence
        }

    except Exception as e:
        logger.error("Trend prediction failed: %s", e)
        return {"success": False, "message": f"Prediction failed: {e}"}
    finally:
        conn.close()

# ------------------------------------------------------------------
if __name__ == "__main__":
    import pandas as pd  # only needed here for Prophet branch
    result = predict_trend("Wireless Headphones", "electronics, audio")
    print(result)