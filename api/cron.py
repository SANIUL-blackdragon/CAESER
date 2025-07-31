import asyncio, requests, sqlite3
from datetime import datetime, timedelta
import sys
import logging
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

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
            conn = sqlite3.connect("./data/caeser.db")
            conn.execute("INSERT INTO error_logs(endpoint, error_msg, timestamp) VALUES (?,?,?)",
                         ("/health", "UP" if ok else "DOWN", datetime.utcnow().isoformat()))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            # Log the database error
            logger.error(f"Failed to log health check result in the database: {str(e)}")

        try:
            # Check for prediction drift and send Discord suggestion if necessary
            conn = sqlite3.connect("./data/caeser.db")
            cur = conn.execute("SELECT COUNT(*) FROM predictions WHERE predicted_uplift > 90")
            if cur.fetchone()[0] > 5:
                try:
                    requests.post("https://discord.com/api/webhooks/...", json={
                        "content": "🤖 Consider adding Google Trends to reduce high-score drift."
                    })
                except requests.RequestException as e:
                    logger.error(f"Failed to send Discord alert: {str(e)}")
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to check prediction drift: {str(e)}")

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