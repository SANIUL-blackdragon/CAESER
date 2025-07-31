"""
affiliate_purchases.py  –  incremental + async-ready skeleton
"""
import asyncio  # kept minimal for future async refactor
import json
import sqlite3
import os
import logging
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
def last_scraped() -> datetime:
    """Return most recent affiliate_data timestamp, or 7 days ago."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT MAX(timestamp) FROM social_data WHERE source='affiliate'"
    )
    ts = cur.fetchone()[0]
    conn.close()
    return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)


# ------------------------------------------------------------------
def init_affiliate_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS affiliate_platforms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform_name TEXT UNIQUE NOT NULL
        )
    """)
    defaults = ["instagram", "facebook", "twitter"]
    for p in defaults:
        cursor.execute(
            "INSERT OR IGNORE INTO affiliate_platforms(platform_name) VALUES (?)", (p,)
        )
    conn.commit()
    conn.close()


# ------------------------------------------------------------------
def fetch_affiliate_data(platform: str):
    url = f"https://api.{platform}.com/v1/data"
    headers = {"Authorization": f"Bearer {os.getenv(f'{platform.upper()}_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error("Failed to fetch %s: %s", platform, e)
        return []


# ------------------------------------------------------------------
def store_affiliate_data():
    init_affiliate_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT platform_name FROM affiliate_platforms")
    platforms = [row[0] for row in cursor.fetchall()]
    conn.close()

    last = last_scraped()
    fresh_rows = []

    for platform in platforms:
        data = fetch_affiliate_data(platform)
        if not data:
            continue

        # keep only rows newer than last stored record
        fresh = [
            row for row in data
            if datetime.fromisoformat(row["timestamp"]) > last
        ]
        if not fresh:
            logger.info("No fresh data for %s", platform)
            continue

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for item in fresh:
            cursor.execute(
                """
                INSERT INTO social_data(text, likes, source, timestamp)
                VALUES (?,?,?,?)
                """,
                (
                    f"{platform}:{item.get('title','')}",
                    item.get("clicks", 0),
                    "affiliate",
                    item["timestamp"],
                ),
            )
        conn.commit()
        conn.close()
        logger.info("Stored %d fresh rows for %s", len(fresh), platform)


# ------------------------------------------------------------------
if __name__ == "__main__":
    init_affiliate_table()
    store_affiliate_data()