import os
from datetime import datetime, timedelta
import logging
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from typing import Dict, Optional, List
import asyncpg

# Optional Prophet import (graceful fallback)
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def _init_connections() -> None:
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS social_data (
                    id SERIAL PRIMARY KEY,
                    source TEXT,
                    text TEXT,
                    likes INTEGER,
                    timestamp TIMESTAMPTZ
                );
                CREATE TABLE IF NOT EXISTS trend_predictions (
                    id SERIAL PRIMARY KEY,
                    product_name TEXT,
                    tags TEXT,
                    predicted_peak_days INTEGER,
                    predicted_peak_date TEXT,
                    confidence REAL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_trend_lookup ON social_data(source, text);
                """
            )
        logger.info("PostgreSQL connected and trend_predictions, social_data tables ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create tables: {e}")
        pg_pool = None

# ------------------------------------------------------------------
async def predict_trend(product_name: str, tags: str) -> Dict:
    """
    Predict trend peak using Holt-Winters or Prophet (if available and data is large).
    """
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot predict trend.")
        return {"success": False, "message": "Database not connected"}

    try:
        async with pg_pool.acquire() as conn:
            tags_list = [tag.strip() for tag in tags.split(",")]
            # Use ILIKE for case-insensitive search and ANY for array matching
            query = """
                SELECT likes, timestamp FROM social_data
                WHERE source='google_trends' AND (text ILIKE $1 OR text = ANY($2::text[]))
                ORDER BY timestamp ASC
            """
            rows = await conn.fetch(query, f"%{product_name}%", tags_list)

            if not rows:
                logger.warning("No trend data for %s (%s)", product_name, tags)
                return {"success": False, "message": "No trend data"}

            likes = np.array([r["likes"] for r in rows], dtype=float)
            timestamps = [r["timestamp"] for r in rows]

            if len(likes) < 3:
                logger.warning("Insufficient data points")
                return {"success": False, "message": "Insufficient data"}

            # --- Model choice ---
            if HAS_PROPHET and len(likes) > 30:
                import pandas as pd # Import pandas here if only used in this branch
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
                peak_days = (peak_row["ds"] - timestamps[-1]).days # type: ignore
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

            await conn.execute("""
                INSERT INTO trend_predictions
                (product_name, tags, predicted_peak_days, predicted_peak_date, confidence, timestamp)
                VALUES ($1, $2, $3, $4, $5, NOW())
            """, product_name, tags, int(peak_days), peak_date, confidence)

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

# ------------------------------------------------------------------
async def init_predict_trend_service():
    await _init_connections()

# ------------------------------------------------------------------
if __name__ == "__main__":
    import asyncio
    async def main():
        await init_predict_trend_service()
        result = await predict_trend("Wireless Headphones", "electronics, audio")
        print(result)
    asyncio.run(main())
