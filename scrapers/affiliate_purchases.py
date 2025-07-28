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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS affiliate_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            clicks INTEGER,
            timestamp TEXT
        )
    """)
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
    platforms = ["instagram", "facebook", "twitter"]  # Example platforms
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

if __name__ == "__main__":
    init_affiliate_table()
    store_affiliate_data()