"""
dark_web.py  –  async + proxy + noise filter + indexing hint
"""
import asyncio
import aiohttp
import sqlite3
import os
import random
import logging
from datetime import datetime
from typing import List, Tuple
import spacy
nlp = spacy.load("en_core_web_sm")

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
PROXY_LIST = (
    os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def fetch_dark(
    session: aiohttp.ClientSession, query: str
) -> List[Tuple[str, int]]:
    proxy = random.choice(PROXY_LIST) if PROXY_LIST else None
    url = f"https://darkweb.example.com/search?q={query}"

    try:
        async with session.get(url, proxy=proxy) as resp:
            if resp.status != 200:
                logger.warning("Bad status %s for query %s", resp.status, query)
                return []
            data = await resp.json()

        # NLP-based relevance + length filter
        posts = []
        query_doc = nlp(query)
        for post in data.get("items", []):
            text_raw = post.get("text", "").strip()
            if not text_raw or len(text_raw.split()) < 3:
                continue
            if nlp(text_raw).similarity(query_doc) < 0.5:
                continue
            posts.append((text_raw, int(post.get("likes", 0))))
        return posts

    except Exception as exc:
        logger.error("Error fetching %s via %s: %s", query, proxy, exc)
        return []

# ------------------------------------------------------------------
async def store_dark(posts: List[Tuple[str, int]]) -> None:
    if not posts:
        return
    conn = sqlite3.connect(DB_PATH)
    with conn:
        # Create index if missing (idempotent)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_social_ts ON social_data(timestamp)"
        )
        conn.executemany(
            "INSERT INTO social_data(text, likes, source, timestamp) "
            "VALUES (?,?,?,?)",
            [
                (text, likes, "dark_web", datetime.utcnow().isoformat())
                for text, likes in posts
            ],
        )
    conn.close()

# ------------------------------------------------------------------
async def main(keywords: List[str]) -> None:
    keywords = [k.strip() for k in keywords if k.strip()]
    if not keywords:
        logger.info("No keywords supplied.")
        return

    logger.info("Dark-web scraping %d keywords via async + proxy", len(keywords))
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=15)
    ) as session:
        tasks = [fetch_dark(session, kw) for kw in keywords]
        results = await asyncio.gather(*tasks)

    flat = [item for sublist in results for item in sublist]
    await store_dark(flat)
    logger.info("Dark-web scrape complete: %d posts stored", len(flat))

# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        kw_input = input("Dark-web keywords (comma-separated): ")
        kw_list = kw_input.split(",")
        asyncio.run(main(kw_list))
    except KeyboardInterrupt:
        logger.info("Aborted by user.")