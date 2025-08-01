#!/usr/bin/env python3
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import text
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_URL = os.getenv("DB_PATH", "postgresql+asyncpg://caeser_user:caeser_pass@localhost:5432/caeser")

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
        for i, (text_val, likes, source) in enumerate(demo_rows, 1):
            await session.execute(
                text("""
                    INSERT INTO social_data(id, platform, post_content, sentiment_score, created_at)
                    VALUES (:id, :platform, :post_content, :sentiment_score, :created_at)
                """),
                {
                    "id": i,
                    "platform": source,
                    "post_content": text_val,
                    "sentiment_score": float(likes),
                    "created_at": datetime.fromisoformat("2025-08-01T02:12:10.651398")
                }
            )
        await session.commit()
    
    print("✅ Demo data loaded into PostgreSQL")

if __name__ == "__main__":
    asyncio.run(load_demo_data())