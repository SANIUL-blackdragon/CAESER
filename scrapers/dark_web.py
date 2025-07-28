# In scrapers/dark_web.py
import json
import sqlite3
import os
from datetime import datetime
import requests

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def init_dark_web_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dark_web_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            likes INTEGER,
            source TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_dark_web_data():
    # Example: Fetch data from a hypothetical dark web API
    url = "https://api.darkweb.com/v1/posts"
    headers = {"Authorization": f"Bearer {os.getenv('DARK_WEB_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch dark web data: {str(e)}")
        return []

def store_dark_web_data():
    data = fetch_dark_web_data()
    if not data:
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for item in data:
        cursor.execute("""
            INSERT INTO dark_web_data (text, likes, source, timestamp)
            VALUES (?, ?, ?, ?)
        """, (item['text'], item['likes'], "dark_web", datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_dark_web_table()
    store_dark_web_data()