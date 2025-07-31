"""
affiliate_purchases.py – real APIs + demo fallback
"""
import asyncio, json, os, logging, csv, aiohttp
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
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
    api_key = os.getenv(f"{platform.upper()}_API_KEY")
    if not api_key:
        logger.warning("No API key for %s – using demo CSV", platform)
        return []
    url = f"https://api.{platform}.com/v1/data"
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
    demo_path = pathlib.Path(__file__).with_name("demo_affiliate.csv")
    if not demo_path.exists():
        return []
    with open(demo_path, newline="", encoding="utf-8") as f:
        return [{"title": row["title"], "clicks": int(row["clicks"]), "timestamp": row["timestamp"]}
                for row in csv.DictReader(f)]

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
            if not data:
                data = await load_demo_csv()
            for row in data:
                try:
                    if datetime.fromisoformat(row["timestamp"]) > last:
                        fresh_rows.append(row)
                except (KeyError, ValueError):
                    continue

        if fresh_rows:
            for item in fresh_rows:
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
            logger.info("Stored %d fresh affiliate rows.", len(fresh_rows))

# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(init_affiliate_table())
    asyncio.run(store_affiliate_data())