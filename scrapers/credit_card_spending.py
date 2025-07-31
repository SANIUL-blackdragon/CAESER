"""
credit_card_spending.py  –  incremental + async-ready skeleton
"""
import sqlite3
import os
import logging
from datetime import datetime, timedelta

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
def last_scraped() -> datetime:
    """Return most recent credit_card timestamp, or 7 days ago."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT MAX(timestamp) FROM social_data WHERE source='credit_card'"
    )
    ts = cur.fetchone()[0]
    conn.close()
    return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)


# ------------------------------------------------------------------
def init_spending_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spending_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            spend_total REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


# ------------------------------------------------------------------
def fetch_credit_card_data():
    url = "https://api.creditcard.com/v1/transactions"
    headers = {"Authorization": f"Bearer {os.getenv('CREDIT_CARD_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error("Credit-card fetch failed: %s", e)
        return []


# ------------------------------------------------------------------
def store_spending_data():
    data = fetch_credit_card_data()
    if not data:
        return

    last = last_scraped()
    fresh = [
        row for row in data
        if datetime.fromisoformat(row["timestamp"]) > last
    ]
    if not fresh:
        logger.info("No fresh credit-card data.")
        return

    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.executemany(
            """
            INSERT INTO social_data(text, likes, source, timestamp)
            VALUES (?,?,?,?)
            """,
            [
                (row["category"], row["spend_total"], "credit_card", row["timestamp"])
                for row in fresh
            ],
        )
    logger.info("Stored %d fresh credit-card rows.", len(fresh))


# ------------------------------------------------------------------
if __name__ == "__main__":
    init_spending_table()
    store_spending_data()