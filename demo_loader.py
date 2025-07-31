#!/usr/bin/env python3
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from datetime import datetime

DB_URL = "postgresql://caeser_user:caeser_pass@localhost:5432/caeser"

async def load_demo_data():
    engine = create_async_engine(DB_URL)
    demo_rows = [
        # Google Trends
        ("sneakers", 78, "google_trends"),
        ("boots", 62, "google_trends"),
        ("electronics", 95, "google_trends"),
        # Affiliate
        ("Nike Air Max 90", 120, "affiliate"),
        ("Adidas Ultraboost 22", 95, "affiliate"),
        # Credit Card
        ("Footwear", 250, "credit_card"),
        ("Electronics", 500, "credit_card"),
        # Dark Web
        ("Limited drop on darknet", 88, "dark_web"),
    ]
    async with AsyncSession(engine) as session:
        for text_val, likes, source in demo_rows:
            await session.execute(
                text("""
                    INSERT INTO social_data(text, likes, source, timestamp)
                    VALUES (:text, :likes, :source, :timestamp)
                """),
                {"text": text_val, "likes": likes, "source": source, "timestamp": datetime.utcnow().isoformat()}
            )
        await session.commit()
    print("✅ Demo data loaded into PostgreSQL")

if __name__ == "__main__":
    asyncio.run(load_demo_data())