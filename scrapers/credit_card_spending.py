"""
credit_card_spending.py  –  incremental + async-ready skeleton
"""
import asyncio
import os
import logging
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
    """Return most recent credit_card timestamp, or 7 days ago."""
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='credit_card'")
        )
        ts = result.scalar()
        return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)


# ------------------------------------------------------------------
async def init_spending_table():
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS spending_data (
                id SERIAL PRIMARY KEY,
                category TEXT,
                spend_total REAL,
                timestamp TEXT
            )
        """))
        await session.commit()


# ------------------------------------------------------------------
async def fetch_credit_card_data():
    url = "https://api.creditcard.com/v1/transactions"
    headers = {"Authorization": f"Bearer {os.getenv('CREDIT_CARD_API_KEY')}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=15) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        logger.error("Credit-card fetch failed: %s", e)
        await discord_service.send_alert_async(f"Credit card scraper failed: {str(e)}")
        return []


# ------------------------------------------------------------------
async def store_spending_data():
    data = await fetch_credit_card_data()
    if not data or not isinstance(data, list):
        return

    last = await last_scraped()
    fresh = []
    for row in data:
        try:
            if datetime.fromisoformat(row["timestamp"]) > last:
                fresh.append(row)
        except (KeyError, ValueError):
            continue
    if not fresh:
        logger.info("No fresh credit-card data.")
        return

    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(
            text("""
                INSERT INTO social_data(text, likes, source, timestamp)
                VALUES (:text, :likes, :source, :timestamp)
            """),
            [
                {"text": row["category"], "likes": row["spend_total"], "source": "credit_card", "timestamp": row["timestamp"]}
                for row in fresh
            ]
        )
        await session.commit()
    logger.info("Stored %d fresh credit-card rows.", len(fresh))
    if len(fresh) > 0:
        await discord_service.send_alert_async(
            f"Credit card scrape success: {len(fresh)} transactions stored"
        )


# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(init_spending_table())
    asyncio.run(store_spending_data())