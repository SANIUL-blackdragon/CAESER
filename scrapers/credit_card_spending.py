"""
credit_card_spending.py – real API + demo CSV fallback
"""
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import asyncio
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
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
    api_key = os.getenv("CREDIT_CARD_API_KEY")
    if not api_key:
        return []
    url = "https://api.creditcard.com/v1/transactions"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=15) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        """Always return [] so demo CSV is used."""
        return []

# ------------------------------------------------------------------
async def load_demo_csv():
    demo_path = pathlib.Path(__file__).with_name("demo_credit.csv")
    if not demo_path.exists():
        return []
    with open(demo_path, newline="", encoding="utf-8") as f:
        return [{"category": row["category"], "spend_total": float(row["spend_total"]), "timestamp": row["timestamp"]}
                for row in csv.DictReader(f)]

# ------------------------------------------------------------------
async def store_spending_data():
    data = await fetch_credit_card_data()
    if not data:
        data = await load_demo_csv()
    last = await last_scraped()
    fresh = [r for r in data if datetime.fromisoformat(r["timestamp"]) > last]
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
            [{"text": row["category"], "likes": int(row["spend_total"]), "source": "credit_card", "timestamp": row["timestamp"]}
             for row in fresh]
        )
        await session.commit()
    logger.info("Stored %d fresh credit-card rows.", len(fresh))

# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(init_spending_table())
    asyncio.run(store_spending_data())