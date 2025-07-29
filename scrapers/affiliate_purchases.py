# In scrapers/affiliate_purchases.py
import json
import sqlite3
import os
from datetime import datetime
import requests

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def init_affiliate_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 1️⃣  create the new dynamic table if it doesn’t exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS affiliate_platforms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform_name TEXT UNIQUE NOT NULL
        )
    """)
    # seed some defaults if table is empty
    defaults = ["instagram", "facebook", "twitter"]
    for p in defaults:
        cursor.execute("INSERT OR IGNORE INTO affiliate_platforms(platform_name) VALUES (?)", (p,))
    conn.commit()
    conn.close()

def fetch_affiliate_data(platform: str):
    # Example: Fetch data from a hypothetical affiliate API
    url = f"https://api.{platform}.com/v1/data"
    headers = {"Authorization": f"Bearer {os.getenv(f'{platform.upper()}_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data from {platform}: {str(e)}")
        return []

def store_affiliate_data():
    init_affiliate_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT platform_name FROM affiliate_platforms")
    platforms = [row[0] for row in cursor.fetchall()]
    conn.close()

    for platform in platforms:
        data = fetch_affiliate_data(platform)
        if not data:
            continue
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for item in data:
            cursor.execute("""
                INSERT INTO affiliate_data (platform, clicks, timestamp)
                VALUES (?, ?, ?)
            """, (platform, item.get('clicks', 0), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        logger.info(f"Stored affiliate data for {platform}")
        logger.info(f"Fetched {len(data)} items from {platform}")
        logger.info(f"Stored {len(data)} items in the database for {platform}")
        logger.info(f"Data stored successfully for {platform}")
        logger.info(f"Data fetch and storage completed for {platform}")
        logger.info(f"Affiliate data for {platform} processed successfully")
        
if __name__ == "__main__":
    init_affiliate_table()
    store_affiliate_data()