"""
google_trends.py – upgraded with pytrends & static fallback
"""
import asyncio
import aiohttp
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Tuple
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
def fetch_trend(keyword: str) -> Tuple[str, int, bool]:
    """
    Use official pytrends if available, else static demo.
    Returns (keyword, score, success_flag).
    """
    if HAS_PYTRENDS:
        try:
            pytrend = TrendReq(hl="en-US", tz=360)
            pytrend.build_payload([keyword], timeframe="today 12-m")
            df = pytrend.interest_over_time()
            score = int(df[keyword].iloc[-1]) if not df.empty else 0
            return keyword, score, True
        except Exception as e:
            logger.error("pytrends failed for %s: %s", keyword, e)
            return keyword, 0, False
    else:
        # static demo fallback
        demo = {"sneakers": 78, "boots": 62, "electronics": 95}
        return keyword, demo.get(keyword.lower(), 50), True

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='google_trends'")
        )
        ts = result.scalar()
        return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)

# ------------------------------------------------------------------
async def needs_refresh(keyword: str, since: datetime) -> bool:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='google_trends' AND text=:keyword"),
            {"keyword": keyword}
        )
        ts = result.scalar()
        if not ts:
            return True
        return datetime.fromisoformat(ts) < datetime.utcnow() - timedelta(hours=12)

# ------------------------------------------------------------------
async def store_trends(rows: List[Tuple[str, int]]) -> None:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(
            text("""
                INSERT INTO social_data(text, likes, source, timestamp)
                VALUES (:text, :likes, :source, :timestamp)
            """),
            [
                {"text": kw, "likes": interest, "source": "google_trends", "timestamp": datetime.utcnow().isoformat()}
                for kw, interest in rows
            ]
        )
        await session.commit()

# ------------------------------------------------------------------
async def main(keywords: List[str]) -> None:
    keywords = [k.strip() for k in keywords if k.strip()]
    if not keywords:
        logger.info("No keywords supplied.")
        return

    since = await last_scraped()
    to_fetch = [kw for kw in keywords if await needs_refresh(kw, since)]
    if not to_fetch:
        logger.info("All keywords are fresh (< 12 h). Nothing to fetch.")
        return

    logger.info("Fetching %d keywords: %s", len(to_fetch), to_fetch)
    results = [fetch_trend(kw) for kw in to_fetch]

    new_rows = [(kw, score) for kw, score, ok in results if ok and score > 0]
    if new_rows:
        await store_trends(new_rows)
        logger.info("Stored %d new trend scores.", len(new_rows))
    else:
        logger.info("No new data returned.")

# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        kw_input = input("Keywords (comma-separated): ")
        kw_list = kw_input.split(",")
        asyncio.run(main(kw_list))
    except KeyboardInterrupt:
        logger.info("Aborted.")