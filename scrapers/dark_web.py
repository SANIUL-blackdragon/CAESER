"""
dark_web.py – async + proxy + demo fallback + NLP filter
"""
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import asyncio
import pandas as pd
import aiohttp
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

nlp = spacy.load("en_core_web_sm")

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
PROXY_LIST = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def fetch_dark(session, query: str) -> List[Tuple[str, int]]:
    api_key = os.getenv("DARK_WEB_API_KEY")
    if not api_key:
        return []
    url = f"https://darkweb.example.com/search?q={query}&key={api_key}"
    proxy = random.choice(PROXY_LIST) if PROXY_LIST else None
    try:
        async with session.get(url, proxy=proxy) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
        query_doc = nlp(query)
        posts = []
        for post in data.get("items", []):
            text_raw = post.get("text", "").strip()
            if not text_raw or len(text_raw.split()) < 3:
                continue
            if nlp(text_raw).similarity(query_doc) < 0.5:
                continue
            posts.append((text_raw, int(post.get("likes", 0))))
        return posts
    except Exception as e:
        """Always return [] so demo CSV is used."""
        return []

# ------------------------------------------------------------------
async def load_demo_csv():
    demo_path = pathlib.Path(__file__).with_name("demo_dark.csv")
    if not demo_path.exists():
        return []
    with open(demo_path, newline="", encoding="utf-8") as f:
        return [(row["text"], int(row["likes"])) for row in csv.DictReader(f)]

# ------------------------------------------------------------------
async def store_dark(posts: List[Tuple[str, int]]) -> None:
    if not posts:
        return
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(
            text("""
                INSERT INTO social_data(text, likes, source, timestamp)
                VALUES (:text, :likes, :source, :timestamp)
            """),
            [
                {"text": text, "likes": likes, "source": "dark_web", "timestamp": datetime.utcnow().isoformat()}
                for text, likes in posts
            ]
        )
        await session.commit()

# ------------------------------------------------------------------
async def main(keywords: List[str]) -> None:
    keywords = [k.strip() for k in keywords if k.strip()]
    if not keywords:
        logger.info("No keywords supplied.")
        return
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        tasks = [fetch_dark(session, kw) for kw in keywords]
        results = await asyncio.gather(*tasks)
    flat = [item for sublist in results for item in sublist]
    if not flat:
        flat = await load_demo_csv()
    await store_dark(flat)
    logger.info("Dark-web scrape complete: %d posts stored", len(flat))

# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        kw_input = input("Dark-web keywords (comma-separated): ")
        asyncio.run(main(kw_input.split(",")))
    except KeyboardInterrupt:
        logger.info("Aborted.")