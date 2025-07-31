"""
google_trends.py  –  async, incremental, drop-in replacement
"""
import asyncio
import aiohttp
import sqlite3
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Tuple

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
        return keyword, 0, False


# ------------------------------------------------------------------
def last_scraped() -> datetime:
    """Return the most recent google_trends timestamp in DB."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT MAX(timestamp) FROM social_data WHERE source='google_trends'"
    )
    ts = cur.fetchone()[0]
    conn.close()
    return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)


# ------------------------------------------------------------------
def needs_refresh(keyword: str, since: datetime) -> bool:
    """Return True if we have no entry or the last entry is older than 12 h."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT MAX(timestamp) FROM social_data WHERE source='google_trends' AND text=?",
        (keyword,),
    )
    ts = cur.fetchone()[0]
    conn.close()
    if not ts:
        return True
    return datetime.fromisoformat(ts) < datetime.utcnow() - timedelta(hours=12)


# ------------------------------------------------------------------
async def store_trends(rows: List[Tuple[str, int]]) -> None:
    """Bulk insert new rows."""
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.executemany(
            "INSERT INTO social_data(text, likes, source, timestamp) VALUES (?,?,?,?)",
            [
                (kw, interest, "google_trends", datetime.utcnow().isoformat())
                for kw, interest in rows
            ],
        )
    conn.close()


# ------------------------------------------------------------------
async def main(keywords: List[str]) -> None:
    """Entry-point for CLI and programmatic use."""
    keywords = [k.strip() for k in keywords if k.strip()]
    if not keywords:
        logger.info("No keywords supplied.")
        return

    since = last_scraped()
    to_fetch = [kw for kw in keywords if needs_refresh(kw, since)]
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