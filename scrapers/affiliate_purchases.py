"""
affiliate_purchases.py  –  incremental + async-ready skeleton
"""
import asyncio
import json
import os
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
    """Return most recent affiliate_data timestamp, or 7 days ago."""
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='affiliate'")
        )
        ts = result.scalar()
        return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)


# ------------------------------------------------------------------
async def init_affiliate_table():
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS affiliate_platforms (
                id SERIAL PRIMARY KEY,
                platform_name TEXT UNIQUE NOT NULL
            )
        """))
        defaults = ["instagram", "facebook", "twitter"]
        for p in defaults:
            await session.execute(
                text("INSERT INTO affiliate_platforms(platform_name) VALUES (:name) ON CONFLICT DO NOTHING"),
                {"name": p}
            )
        await session.commit()


# ------------------------------------------------------------------
async def fetch_affiliate_data(platform: str):
    url = f"https://api.{platform}.com/v1/data"
    headers = {"Authorization": f"Bearer {os.getenv(f'{platform.upper()}_API_KEY')}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=15) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        logger.error("Failed to fetch %s: %s", platform, e)
        await discord_service.send_alert_async(f"Affiliate scraper failed for {platform}: {str(e)}")
        return []


# ------------------------------------------------------------------
async def store_affiliate_data():
    await init_affiliate_table()
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(text("SELECT platform_name FROM affiliate_platforms"))
        platforms = [row[0] for row in result.fetchall()]

        last = await last_scraped()
        fresh_rows = []

        for platform in platforms:
            data = await fetch_affiliate_data(platform)
            if not data or not isinstance(data, list):
                continue

            # keep only rows newer than last stored record
            fresh = []
            for row in data:
                try:
                    if datetime.fromisoformat(row["timestamp"]) > last:
                        fresh.append(row)
                except (KeyError, ValueError):
                    continue
            if not fresh:
                logger.info("No fresh data for %s", platform)
                continue

            for item in fresh:
                await session.execute(
                    text("""
                        INSERT INTO social_data(text, likes, source, timestamp)
                        VALUES (:text, :likes, :source, :timestamp)
                    """),
                    {
                        "text": f"{platform}:{item.get('title','')}",
                        "likes": item.get("clicks", 0),
                        "source": "affiliate",
                        "timestamp": item["timestamp"],
                    }
                )
            await session.commit()
            logger.info("Stored %d fresh rows for %s", len(fresh), platform)
            if len(fresh) > 0:
                await discord_service.send_alert_async(
                    f"Affiliate scrape success: {len(fresh)} rows stored for {platform}"
                )


# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(init_affiliate_table())
    asyncio.run(store_affiliate_data())