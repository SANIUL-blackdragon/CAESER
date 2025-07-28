# In scrapers/social_media_spider.py
import scrapy
import sqlite3
import requests
import json
from datetime import datetime
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import os
import random
from fake_useragent import UserAgent
import time

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
PROXY_LIST = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []

class SqlitePipeline:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO social_data (text, likes, source, timestamp)
            VALUES (?, ?, ?, ?)
        """, (item['text'], item['likes'], item['source'], item['timestamp']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()

class SocialMediaSpider(scrapy.Spider):
    name = "social_media"
    custom_settings = {
        'ITEM_PIPELINES': {'__main__.SqlitePipeline': 1},
        'DOWNLOAD_DELAY': random.uniform(1, 3),
        'ROTATING_PROXY_LIST': PROXY_LIST,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [429, 500, 502, 503, 504]
    }
    ua = UserAgent()

    def __init__(self, sources='reddit,twitter,tiktok,imdb,ebay', target='sneakers', keywords='', *args, **kwargs):
        super(SocialMediaSpider, self).__init__(*args, **kwargs)
        self.sources = [s.strip().lower() for s in sources.split(',')]
        self.target = target
        self.keywords = [kw.strip().lower() for kw in keywords.split(',')] if keywords else []
        self.start_urls = []
        
        if 'reddit' in self.sources:
            self.start_urls.append(f"https://reddit.com/r/{self.target}")
        if 'tiktok' in self.sources:
            self.start_urls.append(f"https://www.tiktok.com/search?q={self.target}")
        if 'instagram' in self.sources:
            self.start_urls.append(f"https://www.instagram.com/explore/tags/{self.target}/")
        if 'imdb' in self.sources:
            self.start_urls.append(f"https://www.imdb.com/search/title/?title_type=feature&genres={self.target}&sort=user_rating,desc")
        if 'ebay' in self.sources:
            self.start_urls.append(f"https://www.ebay.com/sch/i.html?_nkw={self.target}&_sacat=0")
        if 'twitter' not in self.sources:
            return
        
        self.twitter_headers = {
            'Authorization': f'Bearer {TWITTER_API_KEY}',
            'Content-Type': 'application/json'
        }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': self.ua.random}, callback=self.parse)
        
        if 'twitter' in self.sources:
            query = f"{self.target} {' '.join(self.keywords)}" if self.keywords else self.target
            twitter_url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=100"
            yield Request(twitter_url, headers=self.twitter_headers, callback=self.parse_twitter, method='GET')

    def parse(self, response):
        source = 'reddit' if 'reddit' in response.url else 'tiktok' if 'tiktok' in response.url else 'instagram' if 'instagram' in response.url else 'imdb' if 'imdb' in response.url else 'ebay'
        
        if source == 'reddit':
            for post in response.css("div.Post"):
                text = post.css("h3::text").get(default="").strip().lower()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    likes = post.css("div._1rZYMD_4xY3gRcSS3p8ODO::text").get(default="0")
                    yield {
                        "text": text,
                        "likes": int(likes.split()[0]) if likes.isdigit() else 0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
            next_page = response.css("a[rel='nofollow next']::attr(href)").get()
            if next_page:
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})
        
        elif source == 'tiktok':
            count = 0
            for video in response.css("div.tiktok-x6y88p-DivItemContainerV2"):
                if count >= 50:
                    break
                text = video.css("div.tiktok-1qb12g8-DivThreeColumnContainer p::text").get(default="").strip().lower()
                comments = video.css("div.tiktok-1qb12g8-DivCommentContent p::text").getall()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    likes = video.css("strong.tiktok-1p7xrbz-StrongText::text").get(default="0")
                    # Append first 5 comments to text
                    comment_text = " | Comments: " + " ".join(comments[:5]) if comments else ""
                    yield {
                        "text": text + comment_text,
                        "likes": int(likes.replace('K', '000').replace('M', '000000')) if likes else 0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
                count += 1
            next_page = response.css("a.tiktok-1p7xrbz-AButton::attr(href)").get()
            if next_page:
                time.sleep(random.uniform(2, 5))
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})
        
        elif source == 'instagram':
            for post in response.css("article"):
                text = post.css("div._a9zs span::text").get(default="").strip().lower()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    likes = post.css("div.Nm9FK span::text").get(default="0")
                    yield {
                        "text": text,
                        "likes": int(likes.replace(',', '')) if likes.replace(',', '').isdigit() else 0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
        
        elif source == 'imdb':
            count = 0
            for movie in response.css("div.lister-item"):
                if count >= 50:
                    break
                title = movie.css("h3 a::text").get(default="").strip().lower()
                rating = movie.css("div.ratings-bar strong::text").get(default="0")
                if not self.keywords or any(kw in title for kw in self.keywords):
                    yield {
                        "text": title,
                        "likes": float(rating) if rating.replace('.', '').isdigit() else 0.0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
                    count += 1
            next_page = response.css("a.next-page::attr(href)").get()
            if next_page and count < 50:
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})
        
        elif source == 'ebay':
            count = 0
            for item in response.css("li.s-item"):
                if count >= 50:
                    break
                title = item.css("h3.s-item__title::text").get(default="").strip().lower()
                price = item.css("span.s-item__price::text").get(default="0").replace("$", "").replace(",", "").strip()
                if not self.keywords or any(kw in title for kw in self.keywords):
                    yield {
                        "text": title,
                        "likes": float(price) if price.replace('.', '').isdigit() else 0.0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
                    count += 1
            next_page = response.css("a.pagination__next::attr(href)").get()
            if next_page and count < 50:
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})

    def parse_twitter(self, response):
        try:
            data = json.loads(response.text)
            tweets = data.get('data', [])
            for tweet in tweets:
                text = tweet.get('text', '').lower()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    yield {
                        "text": text,
                        "likes": tweet.get('public_metrics', {}).get('like_count', 0),
                        "source": "twitter",
                        "timestamp": datetime.now().isoformat()
                    }
        except json.JSONDecodeError:
            self.logger.error("Failed to parse Twitter response")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Social Media Spider")
    parser.add_argument("--sources", default="reddit,twitter,tiktok,instagram,imdb,ebay", help="Comma-separated sources (e.g., reddit,twitter)")
    parser.add_argument("--target", default="sneakers", help="Target subreddit or query")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    args = parser.parse_args()
    
    process = CrawlerProcess()
    process.crawl(SocialMediaSpider, sources=args.sources, target=args.target, keywords=args.keywords)
    process.start()