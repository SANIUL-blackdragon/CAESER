import scrapy, asyncio, aiohttp, json, os, random, time, logging, pathlib
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

DB_PATH          = os.getenv("DB_PATH", "../data/caeser.db")
PROXY_LIST       = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []
TWITTER_CREDS    = {
    "bearer": os.getenv("TWITTER_BEARER")
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
class SqlitePipeline:
    async def open_spider(self, spider):
        self.engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
        async with AsyncSession(self.engine) as session:
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS social_data(
                    id SERIAL PRIMARY KEY,
                    text TEXT,
                    likes INTEGER,
                    source TEXT,
                    timestamp TEXT
                )
            """))
            await session.commit()

    async def close_spider(self, spider):
        await self.engine.dispose()

    async def process_item(self, item, spider):
        async with AsyncSession(self.engine) as session:
            await session.execute(
                text("""
                    INSERT INTO social_data(text, likes, source, timestamp)
                    VALUES (:text, :likes, :source, :timestamp)
                """),
                {
                    "text": item["text"],
                    "likes": item["likes"],
                    "source": item["source"],
                    "timestamp": item["timestamp"]
                }
            )
            await session.commit()
        return item

# ------------------------------------------------------------------
class DynamicProxyMiddleware:
    """Rotate proxy per request."""
    def process_request(self, request, spider):
        if PROXY_LIST:
            request.meta["proxy"] = random.choice(PROXY_LIST)
        return None

# ------------------------------------------------------------------
class SocialMediaSpider(scrapy.Spider):
    name = "social_media"
    ua = UserAgent()

    custom_settings = {
        "ITEM_PIPELINES": {"__main__.SqlitePipeline": 1},
        "DOWNLOADER_MIDDLEWARES": {
            "__main__.DynamicProxyMiddleware": 350,
            "__main__.Retry429Middleware": 550,
        },
        "DOWNLOAD_DELAY": 1.5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "CONCURRENT_REQUESTS": 32,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 8,
        "RETRY_TIMES": 5,
    }

    def __init__(
        self,
        sources="",
        target="",
        keywords="",
        locations="",
        gender="",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.sources = [s.strip().lower() for s in sources.split(",") if s.strip()]
        self.target = target.strip()
        self.keywords = [k.strip().lower() for k in keywords.split(",") if k.strip()]
        self.locations = [loc.strip().lower() for loc in locations.split(",") if loc.strip()]
        self.gender = gender.strip().lower()

        cfg_path = pathlib.Path(__file__).with_name("scraper_config.json")
        if cfg_path.exists():
            with open(cfg_path, encoding="utf-8") as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {}

        self.start_urls = []
        for src in self.sources:
            if src in self.cfg:
                self.start_urls.append(self.cfg[src]["url"].format(target=self.target))

    # ------------------------------------------------------------------
    def start_requests(self):
        headers = {"User-Agent": self.ua.random}
        for url in self.start_urls:
            yield Request(url, headers=headers, callback=self.parse, dont_filter=True)

        if "twitter" in self.sources and TWITTER_CREDS["bearer"]:
            query = f"{self.target} {' '.join(self.keywords)} {' '.join(self.locations)}"
            yield Request(
                f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=100",
                headers={"Authorization": f"Bearer {TWITTER_CREDS['bearer']}"},
                callback=self.parse_twitter,
                dont_filter=True,
            )

    # ------------------------------------------------------------------
    def parse(self, response):
        source = "reddit" if "reddit" in response.url else "tiktok" if "tiktok" in response.url else "instagram" if "instagram" in response.url else "ebay" if "ebay" in response.url else "imdb"
        parser_map = {
            "reddit": self._parse_reddit,
            "tiktok": self._parse_tiktok,
            "instagram": self._parse_instagram,
            "ebay": self._parse_ebay,
            "imdb": self._parse_imdb,
        }
        yield from parser_map[source](response)

    # ------------------------------------------------------------------
    def _filter_text(self, text):
        if not text or len(text.split()) < 3:
            return None
        return text

    def _parse_reddit(self, response):
        for post in response.css("div.Post"):
            text = post.css("h3::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            likes = int(post.css("div._1rZYMD_4xY3gRcSS3p8ODO::text").get(default="0").split()[0])
            yield {"text": text, "likes": likes, "source": "reddit", "timestamp": datetime.utcnow().isoformat()}

        next_page = response.css("a[rel='nofollow next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def _parse_tiktok(self, response):
        for video in response.css("div.tiktok-x6y88p-DivItemContainerV2"):
            text = video.css("div.tiktok-1qb12g8-DivThreeColumnContainer p::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            likes_str = video.css("strong.tiktok-1p7xrbz-StrongText::text").get(default="0")
            likes = int(likes_str.replace("K", "000").replace("M", "000000")) if likes_str else 0
            yield {"text": text, "likes": likes, "source": "tiktok", "timestamp": datetime.utcnow().isoformat()}

    def _parse_instagram(self, response):
        for post in response.css("article"):
            text = post.css("div._a9zs span::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            likes = int(post.css("div.Nm9FK span::text").get(default="0").replace(",", ""))
            yield {"text": text, "likes": likes, "source": "instagram", "timestamp": datetime.utcnow().isoformat()}

    def _parse_ebay(self, response):
        for item in response.css("li.s-item"):
            text = item.css("h3.s-item__title::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            price = float(
                item.css("span.s-item__price::text")
                .get(default="0")
                .replace("$", "")
                .replace(",", "")
            )
            yield {"text": text, "likes": int(price), "source": "ebay", "timestamp": datetime.utcnow().isoformat()}

    def _parse_imdb(self, response):
        for movie in response.css("div.lister-item"):
            text = movie.css("h3 a::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            rating = float(movie.css("div.ratings-bar strong::text").get(default="0"))
            yield {"text": text, "likes": int(rating * 10), "source": "imdb", "timestamp": datetime.utcnow().isoformat()}

    def parse_twitter(self, response):
        try:
            data = json.loads(response.text)
            for tweet in data.get("data", []):
                text = self._filter_text(tweet.get("text", ""))
                if not text:
                    continue
                yield {
                    "text": text,
                    "likes": tweet.get("public_metrics", {}).get("like_count", 0),
                    "source": "twitter",
                    "timestamp": datetime.utcnow().isoformat(),
                }
        except json.JSONDecodeError:
            logger.error("Invalid Twitter JSON response")

# ------------------------------------------------------------------
class Retry429Middleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        response = reason.value.response if hasattr(reason, "value") else None
        if response and response.status == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            spider.logger.info(f"429 received, retrying after {retry_after}s")
            time.sleep(retry_after)
        return super().retry(request, reason, spider)

# Append right after the existing Retry429Middleware class in social_media_spider.py
class AdaptiveBackoffMiddleware:
    """429/503 aware with exponential back-off and jitter."""
    def __init__(self, backoff_base=1.0):
        self.backoff_base = backoff_base

    @classmethod
    def from_crawler(cls, crawler):
        return cls(backoff_base=crawler.settings.getfloat("BACKOFF_BASE", 1.0))

    def process_response(self, request, response, spider):
        if response.status in {429, 503}:
            retry_after = int(response.headers.get("Retry-After", 60))
            jitter = random.uniform(0.5, 1.5)
            delay = retry_after * jitter
            spider.logger.info("AdaptiveBackoff: sleeping %.1fs", delay)
            time.sleep(delay)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def _retry(self, request, reason, spider):
        # re-use scrapy’s built-in retry
        from scrapy.downloadermiddlewares.retry import RetryMiddleware as RM
        return RM.retry(self, request, reason, spider)

# ---- add to custom_settings ----
# DOWNLOADER_MIDDLEWARES  += {"__main__.AdaptiveBackoffMiddleware": 560}
# ------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default="reddit,twitter,tiktok,instagram,ebay,imdb")
    parser.add_argument("--target", required=True)
    parser.add_argument("--keywords", default="")
    parser.add_argument("--locations", default="")
    parser.add_argument("--gender", default="")
    args = parser.parse_args()

    process = CrawlerProcess()
    process.crawl(
        SocialMediaSpider,
        sources=args.sources,
        target=args.target,
        keywords=args.keywords,
        locations=args.locations,
        gender=args.gender,
    )
    process.start()