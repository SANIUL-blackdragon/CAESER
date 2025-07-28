# In scrapers/google_trends.py
import requests
import sqlite3
import os
from datetime import datetime
from time import sleep

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def get_google_trends(keywords):
    results = []
    url = f"https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=300&geo=US&cat=all&ed={datetime.now().strftime('%Y%m%d')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            trends = data['default']['trendingSearchesDays'][0]['trendingSearches']
            for keyword in keywords:
                keyword = keyword.strip().lower()
                interest = 0
                for trend in trends:
                    if keyword in trend['title']['query'].lower():
                        interest = int(trend['formattedTraffic'].replace('K', '000').replace('M', '000000')) or 0
                        break
                results.append((keyword, interest))
            return results
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Google Trends data (attempt {attempt + 1}/{retries}): {str(e)}")
            sleep(2 ** attempt)  # Exponential backoff
    return results

def store_trend(keyword, interest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO social_data (text, likes, source, timestamp)
        VALUES (?, ?, ?, ?)
    """, (keyword, interest, "google_trends", datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    keywords = input("Enter keywords (comma-separated): ").split(",")
    trends = get_google_trends(keywords)
    for keyword, interest in trends:
        store_trend(keyword, interest)