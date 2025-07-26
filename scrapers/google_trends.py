import requests
import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def get_google_trends(keywords):
    results = []
    url = f"https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=300&geo=US&cat=all&ed={datetime.now().strftime('%Y%m%d')}"
    response = requests.get(url)
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