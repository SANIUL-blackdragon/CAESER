"""
google_trends.py  –  async, incremental, drop-in replacement
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

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def fetch_trend(
    session: aiohttp.ClientSession, keyword: str
) -> Tuple[str, int, bool]:
    """
    Fetch Google-Trends interest score for a single keyword.
    Returns (keyword, score, success_flag).
    Uses the free lightweight endpoint that returns JSONP.
    """
    url = (
        "https://trends.googleapis.com/trends/api/explore"
        f"?hl=en-US&tz=-120"
        f'&req={{"comparisonItem":[{{"keyword":"{keyword}","geo":"","time":"today 12-m"}}],"category":0}}'
        "&token=APP6_UEAAAAAZLm9o&tz=-120"
    )
    try:
        async with session.get(url, timeout=15) as resp:
            if resp.status != 200:
                logger.warning("HTTP %s for keyword %s", resp.status, keyword)
                return keyword, 0, False
            text = await resp.text()
            # Strip JSONP wrapper
            if ")]}'," in text:
                core = text.split(")]}',", 1)[1]
                data = json.loads(core)
                # last data point
                timeline = data.get("default", {}).get("timelineData", [])
                if timeline:
                    interest = timeline[-1]["value"][0]
                    return keyword, int(interest), True
            return keyword, 0, False
    except aiohttp.ClientError as e:
        logger.error("Network error fetching %s: %s", keyword, e)
        return keyword, 0, False
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON for %s: %s", keyword, e)
        return keyword, 0, False
    except Exception as e:
        logger.error("Unexpected error fetching %s: %s", keyword, e)
        await discord_service.send_alert_async(f"Google Trends scraper failed for {keyword}: {str(e)}")
        return keyword, 0, False


# ------------------------------------------------------------------
async def last_scraped() -> datetime:
    """Return the most recent google_trends timestamp in DB."""
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='google_trends'")
        )
        ts = result.scalar()
        return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)


# ------------------------------------------------------------------
async def needs_refresh(keyword: str, since: datetime) -> bool:
    """Return True if we have no entry or the last entry is older than 12 h."""
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
    """Bulk insert new rows."""
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
    """Entry-point for CLI and programmatic use."""
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
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=10), timeout=aiohttp.ClientTimeout(total=30)
    ) as session:
        tasks = [fetch_trend(session, kw) for kw in to_fetch]
        results = await asyncio.gather(*tasks)

    # --- monitoring ---
    total = len(results)
    successes = sum(1 for _, _, ok in results if ok)
    failure_ratio = (total - successes) / total if total else 0
    if failure_ratio > 0.3:
        logger.warning(
            "High failure ratio: %.1f%% (%d/%d) – please investigate.",
            failure_ratio * 100,
            total - successes,
            total,
        )
    # ------------------

    new_rows = [(kw, score) for kw, score, ok in results if ok and score > 0]
    if new_rows:
        await store_trends(new_rows)
        logger.info("Stored %d new trend scores.", len(new_rows))
        if new_rows:
            await discord_service.send_alert_async(
                f"Google Trends scrape success: {len(new_rows)} scores stored"
            )
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