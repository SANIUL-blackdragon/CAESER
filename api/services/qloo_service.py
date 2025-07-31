# api/services/qloo_service.py
import os
import json
import asyncio
import aiohttp
import logging
import re
from typing import Dict, List, Optional
import asyncpg
import redis.asyncio as redis
from cachetools import TTLCache

# -------------------- Logging --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------- Redis (primary cache) --------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client: Optional[redis.Redis] = None

# -------------------- PostgreSQL (second-level cache) ----------
POSTGRES_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)
pg_pool: Optional[asyncpg.Pool] = None

# -------------------- In-Memory fallback ------------------------
memory_cache = TTLCache(maxsize=100, ttl=3600)

# -------------------- Constants ---------------------------------
QLOO_API_KEY = os.getenv("QLOO_API_KEY")
BASE_URL = "https://hackathon.api.qloo.com/v2/insights"

# -------------------- Helpers ----------------------------------
def sanitize_input(input_str: str) -> str:
    """Remove any non-alphanumeric characters except space, comma, period, hyphen."""
    return re.sub(r"[^a-zA-Z0-9\s,.-]", "", input_str.strip())

# >>>>> GRANULAR CACHE KEY (already deterministic) <<<<<
def _build_cache_key(insight_type: str, location: str, tags: List[str]) -> str:
    tag_csv = ",".join(sorted(tags))  # keep it deterministic
    return f"qloo:{insight_type}:{location}:{tag_csv}"

def _build_params(insight_type: str, location: str, tags: List[str]) -> Dict[str, Optional[str]]:
    filter_tags = ",".join([f"urn:tag:keyword:brand:{tag.lower()}" for tag in tags])
    params: Dict[str, Optional[str]] = {}

    if insight_type == "brand":
        params.update({
            "filter.type": "urn:entity:brand",
            "signal.location.query": location if location != "global" else None,
            "filter.tags": filter_tags
        })
    elif insight_type == "demographics":
        params.update({
            "filter.type": "urn:demographics",
            "signal.location.query": location if location != "global" else None,
            "signal.interests.tags": filter_tags
        })
    elif insight_type == "heatmap":
        params.update({
            "filter.type": "urn:heatmap",
            "filter.location.query": location if location != "global" else None,
            "signal.interests.tags": filter_tags
        })
    else:
        raise ValueError(f"Unsupported insight type: {insight_type}")
    return params

# -------------------- Async retry wrapper ----------------------
async def _retry_async(coro, max_attempts: int = 3, base_delay: float = 1.0):
    attempt = 0
    while True:
        try:
            return await coro
        except Exception as e:
            attempt += 1
            if attempt >= max_attempts:
                raise
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning("Retrying in %.1fs after failure: %s", delay, e)
            await asyncio.sleep(delay)

# -------------------- Cache helpers -----------------------------
async def _get_cache(key: str) -> Optional[Dict]:
    """Redis → PostgreSQL → memory fall-through."""
    # 1. Redis
    if redis_client:
        try:
            cached = await redis_client.get(key)
            if cached:
                logger.info("Cache hit (Redis) for %s", key)
                return json.loads(cached)
        except Exception as e:
            logger.warning("Redis read failed: %s", e)

    # 2. PostgreSQL
    if pg_pool:
        try:
            async with pg_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT value FROM qloo_cache WHERE key = $1", key
                )
                if row:
                    logger.info("Cache hit (PostgreSQL) for %s", key)
                    return json.loads(row["value"])
        except Exception as e:
            logger.warning("PostgreSQL read failed: %s", e)

    # 3. In-memory
    if key in memory_cache:
        logger.info("Cache hit (memory) for %s", key)
        return memory_cache[key]

    return None

async def _set_cache(key: str, value: Dict, ttl: int = 3600) -> None:
    """Write-through to Redis, PostgreSQL and memory."""
    payload = json.dumps(value)

    # 1. Redis
    if redis_client:
        try:
            await redis_client.setex(key, ttl, payload)
        except Exception as e:
            logger.warning("Redis write failed: %s", e)

    # 2. PostgreSQL
    if pg_pool:
        try:
            async with pg_pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO qloo_cache(key, value, expires_at)
                    VALUES ($1, $2, NOW() + INTERVAL '1 hour')
                    ON CONFLICT (key) DO UPDATE
                    SET value = EXCLUDED.value,
                        expires_at = EXCLUDED.expires_at
                    """,
                    key, payload
                )
        except Exception as e:
            logger.warning("PostgreSQL write failed: %s", e)

    # 3. Memory
    memory_cache[key] = value

# -------------------- Connection initializers -------------------
async def _init_connections() -> None:
    """Called once at startup (see bottom)."""
    global redis_client, pg_pool

    # Redis
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning("Redis unavailable: %s", e)
        redis_client = None

    # PostgreSQL
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        # ensure table exists
        async with pg_pool.acquire() as conn: #type: ignore
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS qloo_cache (
                    key TEXT PRIMARY KEY,
                    value JSONB NOT NULL,
                    expires_at TIMESTAMPTZ NOT NULL
                )
                """
            )
        logger.info("PostgreSQL connected")
    except Exception as e:
        logger.warning("PostgreSQL unavailable: %s", e)
        pg_pool = None

# -------------------- Main service call -------------------------
async def get_cultural_insights(
    location: str,
    tags: List[str],
    insight_type: str = "brand"
) -> Dict:
    # ---------- Validation ----------
    if not QLOO_API_KEY:
        raise ValueError("QLOO_API_KEY not configured")

    if not location or not isinstance(location, str) or not location.strip():
        raise ValueError("Invalid location provided")

    if not tags or not isinstance(tags, list) or not all(isinstance(t, str) and t.strip() for t in tags):
        raise ValueError("Invalid tags provided")

    location = sanitize_input(location)
    tags = [sanitize_input(tag) for tag in tags]

    cache_key = _build_cache_key(insight_type, location, tags)

    # >>>>> ASYNC TWEAK: immediate cache return <<<<<
    cached = await _get_cache(cache_key)
    if cached:
        return cached

    # ---------- Build Request ----------
    params = _build_params(insight_type, location, tags)
    headers = {
        "X-Api-Key": QLOO_API_KEY,
        "Content-Type": "application/json"
    }

    # ---------- Async HTTP Call with Retry ----------
    async def _fetch():
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
        ) as session:
            async with session.get(BASE_URL, headers=headers, params=params) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise ValueError(f"Qloo API error {resp.status}: {text}")
                data = await resp.json()
                if not data.get("success"):
                    raise ValueError(f"Invalid API response: {data.get('message', 'Unknown error')}")
                return data

    try:
        data = await _retry_async(_fetch())
    except Exception as e:
        logger.error("Qloo API request failed: %s", e)
        return {"success": False, "data": None, "message": str(e)}

    # ---------- Cache & Return ----------
    result = {
        "success": True,
        "data": data.get("results"),
        "message": f"{insight_type.capitalize()} insights retrieved successfully"
    }

    await _set_cache(cache_key, result, ttl=3600)
    logger.info("Cached insights for %s", cache_key)
    return result

# -------------------- Module-level startup hook -----------------
# If you have an ASGI lifespan-handler (FastAPI/Starlette),
# call _init_connections() there instead.
if __name__ != "__main__":
    asyncio.create_task(_init_connections())

# ------------------------------------------------------------------
# NEW ASYNC WRAPPER
# ------------------------------------------------------------------
async def get_cultural_insights_async(location, tags, insight_type="brand"):
    return await get_cultural_insights(location, tags, insight_type)