# api/main.py  –  v3 + semaphore + AWS Secrets Manager
import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

# api/main.py (ADD AT TOP)
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import boto3
import numpy as np
import pandas as pd
from celery import Celery
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, select, text, Table, MetaData, Column, String, Float, Integer, JSON, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
import redis.asyncio as redis
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Import the unchanged service layer
from .services import (
    data_quality_service,
    discord_service,
    hype_engine,
    integrations_service,
    llm_service,
    qloo_service,
    init_qloo_service,
    init_data_quality_service,
    init_discord_service,
    init_hype_engine_service,
    init_llm_service,
    init_predict_trend_service,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------- SECRETS ----------
secrets = boto3.client(
    "secretsmanager",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

def get_secret(name: str, fallback: Optional[str] = None) -> str: #type: ignore
    """Always return a string (never dict or None)."""
    try:
        val = json.loads(secrets.get_secret_value(SecretId=name)["SecretString"])
        if isinstance(val, dict):
            # if the secret itself is a JSON blob, stringify it
            return json.dumps(val)
        return str(val)
    except Exception:
        return str(os.getenv(name, fallback or ""))

DB_URL       = get_secret("caeser-db-url")
REDIS_URL    = get_secret("caeser-redis-url")
QLOO_API_KEY = os.getenv("QLOO_API_KEY")
OPENROUTER = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENROUTER_API_KEY"] = OPENROUTER  # Critical for LLM service


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# ---------- SERVICES ----------
engine = create_async_engine(
    DB_URL, pool_pre_ping=True, pool_size=10, max_overflow=20
)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# ---------- DATABASE TABLES ----------
metadata = MetaData()

competitors = Table(
    "competitors",
    metadata,
    Column("name", String, primary_key=True),
    Column("hype_score", Float, nullable=False),
)

categories = Table(
    "categories",
    metadata,
    Column("category_name", String, primary_key=True),
    Column("keywords", String),
)

# ---------- FASTAPI ----------
app = FastAPI(title="CÆSER API v3")

# ---------- CELERY SETUP ----------
celery_app = Celery(
    "caeser",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)
celery_app.conf.task_default_queue = "scraping"
celery_app.conf.task_routes = {
    "api.main.run_scrapy": {"queue": "scraping"}
}

# ---------- GLOBAL EXCEPTION HANDLER ----------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception at %s: %s", request.url, exc, exc_info=True
    )
    return JSONResponse(
        status_code=500, content={"detail": "Internal server error"}
    )

# ---------- MODELS ----------
class LogMessageIn(BaseModel):
    new_message: str

class CompetitorIn(BaseModel):
    name: str
    hype_score: float

class CategoryIn(BaseModel):
    category_name: str
    keywords: str  # comma-separated

class AnalyzeInput(BaseModel):
    product_name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    tags: str = Field(..., min_length=1)
    target_area: Optional[str] = None
    locations: Optional[str] = None
    gender: Optional[str] = None
    sources: Optional[str] = None

class RetrainOut(BaseModel):
    success: bool
    message: str
    new_weights: dict

# ---------- UTIL ----------
async def init_db_indexes() -> None:
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS competitors (
                    name TEXT PRIMARY KEY,
                    hype_score REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    product_name TEXT,
                    data JSONB
                );
                CREATE TABLE IF NOT EXISTS hype_scores (
                    id SERIAL PRIMARY KEY,
                    score REAL,
                    sentiment REAL,
                    category TEXT,
                    location TEXT,
                    product_name TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS outcomes (
                    id SERIAL PRIMARY KEY,
                    prediction_id INTEGER,
                    actual_uplift REAL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS model_weights (
                    key TEXT PRIMARY KEY,
                    value REAL
                );
                CREATE TABLE IF NOT EXISTS categories (
                    category_name TEXT PRIMARY KEY,
                    keywords TEXT
                );
                CREATE TABLE IF NOT EXISTS social_data (
                    id SERIAL PRIMARY KEY,
                    source TEXT,
                    text TEXT,
                    likes INTEGER,
                    timestamp TIMESTAMPTZ
                );
                """
            )
        )

# ---------- CACHED QLOO with granular key ----------
async def cached_qloo(
    location: str, tags: str, insight_type: str = "brand"
) -> Dict:
    tag_list = sorted(tags.split(","))
    key = f"qloo:{insight_type}:{location}:{tag_list}"
    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)

    result = await qloo_service.get_cultural_insights_async(
        location, tag_list, insight_type
    )
    await redis_client.setex(key, 3600, json.dumps(result))
    return result

# ---------- TREND PREDICTION ----------
async def predict_trend(product_name: str, tags: str) -> Dict:
    try:
        tag_list = tags.split(",")
        async with AsyncSessionLocal() as session:
            query = text(
                """
                SELECT likes, timestamp
                FROM social_data
                WHERE source='google_trends' AND text = ANY(:tags)
                ORDER BY timestamp
                """
            )
            rows = (
                await session.execute(query, {"tags": tag_list})
            ).fetchall()

        if len(rows) < 3:
            return {"success": False, "message": "Insufficient trend data"}

        df = pd.DataFrame(rows, columns=["likes", "timestamp"])
        df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0)
        model = ExponentialSmoothing(
            df["likes"], trend="add", seasonal=None
        ).fit()
        forecast = model.forecast(90)
        peak_idx = int(np.argmax(forecast))
        peak_date = (
            pd.Timestamp.utcnow() + pd.Timedelta(days=peak_idx)
        ).strftime("%Y-%m-%d")

        return {
            "success": True,
            "predicted_peak_days": peak_idx + 1,
            "predicted_peak_date": peak_date,
            "confidence": max(
                0.0, 1 - model.sse / (df["likes"] ** 2).sum()
            ),
        }

    except Exception as e:
        logger.exception("Trend prediction failed")
        return {"success": False, "message": str(e)}

# ---------- STARTUP ----------
@app.on_event("startup")
async def startup_event():
    await init_db_indexes()
    await init_qloo_service()
    await init_data_quality_service()
    await init_discord_service()
    await init_hype_engine_service()
    await init_llm_service()
    await init_predict_trend_service()
    await FastAPILimiter.init(redis_client)
    Instrumentator().instrument(app).expose(app)
    logger.info(os.getenv("STARTUP_MESSAGE", "CÆSER API v3 live 🚀"))

# ---------- ENDPOINTS ----------
# ---------- CELERY TASK ----------
@celery_app.task(name="api.main.run_scrapy")
async def run_scrapy(
    product_name: str,
    sources: str,
    tags: str,
    locations: str = None, #type: ignore
    gender: str = None, #type: ignore
):
    cmd = [
        "scrapy",
        "crawl",
        "social_media",
        "-a",
        f"target={product_name}",
        "-a",
        f"sources={sources}",
        "-a",
        f"keywords={tags}",
    ]
    if locations:
        cmd.extend(["-a", f"locations={locations}"])
    if gender:
        cmd.extend(["-a", f"gender={gender}"])

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise Exception(f"Scraping failed: {stderr.decode()}")
    return stdout.decode()

@app.post(
    "/analyze",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def analyze_endpoint(inp: AnalyzeInput):
    start = time.time()
    try:
        # Queue the scraping task
        task = run_scrapy.delay(
            product_name=inp.product_name,
            sources=inp.sources or "reddit,tiktok,instagram,imdb,ebay",
            tags=inp.tags,
            locations=inp.locations,
            gender=inp.gender,
        )

        # Continue with other processing while scraping runs in background
        hype = await hype_engine.calculate_hype_score_async(
            {},
            inp.tags,
            inp.target_area or "global",
            20.0,
            inp.product_name,
        )

        trend = await predict_trend(inp.product_name, inp.tags)

        return {
            "success": True,
            "hype_score": hype.get("averageScore", 0),
            "trend_prediction": trend if trend.get("success") else None,
            "message": "Analysis completed (scraping queued)",
            "task_id": task.id,
        }

    except Exception as e:
        logger.exception("Unhandled error in /analyze")
        return {
            "success": False,
            "message": "Internal server error",
            "error": str(e),
        }
    finally:
        logger.info("/analyze took %.1f ms", (time.time() - start) * 1000)

# ---------- Legacy endpoints ----------
@app.post("/admin/log_message")
async def set_log_message(body: LogMessageIn):
    os.environ["STARTUP_MESSAGE"] = body.new_message
    return {"success": True, "message": "Next restart will use the new message"}

@app.get("/competitors")
async def competitors():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(competitors))
        rows = result.fetchall()
    return {r.name: {"hype": r.hype_score} for r in rows}

@app.post(
    "/competitors/add",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def add_competitor(body: CompetitorIn):
    async with AsyncSessionLocal() as session:
        stmt = insert(competitors).values(
            name=body.name, hype_score=body.hype_score
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["name"],
            set_=dict(hype_score=body.hype_score),
        )
        await session.execute(stmt)
        await session.commit()
    return {
        "success": True,
        "message": f"Competitor {body.name} saved/updated",
    }

@app.post(
    "/categories",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def add_or_update_category(body: CategoryIn):
    async with AsyncSessionLocal() as session:
        stmt = insert(categories).values(
            category_name=body.category_name, keywords=body.keywords
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["category_name"],
            set_=dict(keywords=body.keywords),
        )
        await session.execute(stmt)
        await session.commit()
    return {
        "success": True,
        "message": f"Category '{body.category_name}' saved",
    }

@app.get("/categories")
async def list_categories():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(categories))
        rows = result.fetchall()
    return {
        "success": True,
        "data": {r.category_name: r.keywords.split(",") for r in rows},
    }

@app.get("/insights/{location}")
async def get_insights(
    location: str, tags: str, insight_type: str = "brand"
):
    return await cached_qloo(location, tags, insight_type)

@app.get("/llm_data_quality")
async def get_llm_data_quality():
    return await llm_service.get_llm_data_quality_async()

@app.get("/data_quality")
async def get_data_quality():
    return await data_quality_service.check_data_quality_async()

@app.post("/predict/demand")
async def predict_demand(data: dict) -> dict:
    return await llm_service.get_prediction_async(
        data.get("product", {}),
        data.get("insights", {}),
        data.get("hype_score", 0),
    )

@app.post("/hype/score")
async def calculate_hype_score(data: dict) -> dict:
    return await hype_engine.calculate_hype_score_async(
        data.get("insights", {}),
        data.get("category", ""),
        data.get("location", ""),
        20.0,
    )

@app.post("/discord/alert")
async def send_discord_alert(data: dict):
    return await discord_service.send_alert_async(
        data.get("prediction"), data.get("hype_data")
    )

@app.post("/integrations/send")
async def send_integrations(data: dict):
    return await integrations_service.send_integrations_async(
        data.get("prediction"), data.get("hype_data")
    )

@app.get("/hype/history/{location}/{category}")
async def get_hype_history(location: str, category: str):
    async with AsyncSessionLocal() as session:
        rows = (
            await session.execute(
                text(
                    """
                    SELECT score, created_at
                    FROM hype_scores
                    WHERE category = :cat AND location = :loc
                    ORDER BY created_at
                    """
                ),
                {"cat": category, "loc": location},
            )
        ).fetchall()
    return {
        "success": True,
        "data": [{"score": r[0], "timestamp": r[1]} for r in rows],
    }

@app.post("/submit_outcome")
async def submit_outcome(data: dict):
    pid = data.get("prediction_id")
    uplift = data.get("actual_uplift")
    if not isinstance(pid, int) or pid <= 0:
        raise HTTPException(
            status_code=400, detail="Bad prediction_id"
        )
    if uplift is None or not isinstance(uplift, (int, float)):
        raise HTTPException(
            status_code=400, detail="Bad actual_uplift"
        )
    async with AsyncSessionLocal() as session:
        await session.execute(
            text(
                """
                INSERT INTO outcomes(prediction_id, actual_uplift, timestamp)
                VALUES (:pid, :uplift, :ts)
                """
            ),
            {"pid": pid, "uplift": uplift, "ts": datetime.utcnow()},
        )
        await session.commit()
    return {"success": True, "message": "Outcome submitted"}

@app.post("/retrain", response_model=RetrainOut)
async def retrain_endpoint():
    async with AsyncSessionLocal() as session:
        rows = (
            await session.execute(
                text(
                    """
                    SELECT h.sentiment, o.actual_uplift
                    FROM hype_scores h
                    JOIN outcomes o ON o.prediction_id = h.id
                    ORDER BY h.created_at DESC
                    LIMIT 100
                    """
                )
            )
        ).fetchall()
        if not rows:
            return RetrainOut(
                success=False,
                message="Need ≥1 outcome to retrain",
                new_weights={},
            )
        sentiments = [r[0] for r in rows]
        actuals = [r[1] for r in rows]
        new_weight = sum(actuals) / (sum(sentiments) + 1e-9)
        await session.execute(
            text(
                """
                INSERT INTO model_weights(key, value)
                VALUES ('sentiment_weight', :val)
                ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value
                """
            ),
            {"val": new_weight},
        )
        await session.commit()
    return RetrainOut(
        success=True,
        message="Weights updated",
        new_weights={"sentiment_weight": new_weight},
    )

@app.get("/health")
async def health_check():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok"}
