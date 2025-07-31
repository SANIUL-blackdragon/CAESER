import asyncio
import requests
from datetime import datetime, timedelta
import sys
import logging
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def health_check_loop():
    while True:
        try:
            # Perform the health check
            r = requests.get("http://localhost:8000/health", timeout=5)
            ok = r.status_code == 200
        except requests.RequestException as e:
            # Log the exception if the request fails
            logger.error(f"Health check request failed: {str(e)}")
            ok = False
        except Exception as e:
            # Log any other unexpected exceptions
            logger.error(f"Unexpected error during health check: {str(e)}")
            ok = False

        try:
            # Log the health check result in the database
            db_url = os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser")
            engine = create_async_engine(db_url, echo=False)
            async with AsyncSession(engine) as session:
                try:
                    await session.execute(
                        text("INSERT INTO error_logs(endpoint, error_msg, timestamp) VALUES (:endpoint, :msg, :ts)"),
                        {"endpoint": "/health", "msg": "UP" if ok else "DOWN", "ts": datetime.utcnow().isoformat()}
                    )
                    await session.commit()
                except Exception as e:
                    logger.error(f"Failed to log health check result in the database: {str(e)}")
                    await session.rollback()

        try:
            # Check for prediction drift and send Discord suggestion if necessary
            db_url = os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser")
            engine = create_async_engine(db_url, echo=False)
            async with AsyncSession(engine) as session:
                try:
                    result = await session.execute(
                        text("SELECT COUNT(*) FROM predictions WHERE predicted_uplift > 90")
                    )
                    count = result.scalar() or 0
                    if count > 5:
                        try:
                            requests.post("https://discord.com/api/webhooks/...", json={
                                "content": "🤖 Consider adding Google Trends to reduce high-score drift."
                            })
                        except requests.RequestException as e:
                            logger.error(f"Failed to send Discord alert: {str(e)}")
                except Exception as e:
                    logger.error(f"Failed to check prediction drift: {str(e)}")
                    await session.rollback()

        # Sleep for 5 minutes before the next health check
        await asyncio.sleep(300)
        
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
if webhook_url:
    try:
        requests.post(webhook_url, json={
            "content": "🤖 Consider adding Google Trends to reduce high-score drift."
        }, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Failed to send Discord alert: {str(e)}")

# Add this to run the health check loop when executed as a module
if __name__ == "__main__":
    print("Starting health monitoring service...")
    print("Press Ctrl+C to stop")
    try:
        asyncio.run(health_check_loop())
    except KeyboardInterrupt:
        print("\nHealth monitoring stopped")
        sys.exit(0)