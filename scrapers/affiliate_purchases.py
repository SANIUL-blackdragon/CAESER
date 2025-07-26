# In scrapers/affiliate_purchases.py
import json
import sqlite3
import os
from datetime import datetime

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

def store_affiliate_data():
    mock_data = [{"platform": "instagram", "clicks": 200}]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for item in mock_data:
        cursor.execute("""
            INSERT INTO affiliate_data (platform, clicks, timestamp)
            VALUES (?, ?, ?)
        """, (item['platform'], item['clicks'], datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_affiliate_table()
    store_affiliate_data()