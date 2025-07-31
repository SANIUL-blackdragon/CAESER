# data/init_db.py
"""
PostgreSQL + SQLAlchemy bootstrap (ORM edition).
Keeps Alembic first, then falls back to ORM for anything missing.
"""
import os
import logging
from datetime import datetime, timedelta

from sqlalchemy import (
    create_engine, MetaData, Column,
    Integer, String, Float, DateTime, Text, CheckConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from alembic import config, command

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# PostgreSQL connection
# ------------------------------------------------------------------
DB_URL = os.getenv("DB_PATH")  # postgresql+psycopg2://user:pass@host:5432/db
if not DB_URL:
    raise RuntimeError("Environment variable DB_PATH is required (PostgreSQL URL).")

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)
Base = declarative_base()

# ------------------------------------------------------------------
# ORM Models
# ------------------------------------------------------------------
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category_name = Column(String, index=True)


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, index=True)
    category = Column(String)
    predicted_uplift = Column(Float)
    confidence = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class SocialData(Base):
    __tablename__ = "social_data"
    __table_args__ = (
        {"postgresql_partition_by": "RANGE (timestamp)"}
    )
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    likes = Column(Integer)
    source = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class CulturalInsight(Base):
    __tablename__ = "cultural_insights"
    id = Column(Integer, primary_key=True)
    location = Column(String, index=True)
    insight_type = Column(String)
    value = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Competitor(Base):
    __tablename__ = "competitors"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    website = Column(String)
    hype_score = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "hype_score >= 0 AND hype_score <= 100",
            name="hype_range"
        ),
    )


class InsightType(Base):
    __tablename__ = "insight_types"
    id = Column(Integer, primary_key=True)
    type_name = Column(String, unique=True, nullable=False)


# ------------------------------------------------------------------
# Utility: create missing tables via ORM
# ------------------------------------------------------------------
def create_missing_tables():
    """Create tables that Alembic has not produced yet."""
    Base.metadata.create_all(engine, checkfirst=True)
    logger.info("ORM tables ensured.")


# ------------------------------------------------------------------
# Utility: seed insight_types defaults
# ------------------------------------------------------------------
def seed_insight_types():
    defaults = ["brand", "demographics", "heatmap"]
    with SessionLocal() as session:
        for t in defaults:
            session.merge(InsightType(type_name=t))
        session.commit()
    logger.info("Insight types seeded.")


# ------------------------------------------------------------------
# Utility: create extra objects if Alembic skipped them
# ------------------------------------------------------------------
def create_post_migration_objects():
    with engine.begin() as conn:
        # 2025 partition
        conn.execute(sa.text("""
            CREATE TABLE IF NOT EXISTS social_data_2025
            PARTITION OF social_data
            FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
        """))

        # View
        conn.execute(sa.text("""
            CREATE OR REPLACE VIEW avg_hype_per_category AS
            SELECT category, AVG(predicted_uplift) AS avg_hype
            FROM predictions
            GROUP BY category;
        """))

        # Validate constraints after ensuring data is clean
        conn.execute(sa.text("""
            ALTER TABLE competitors VALIDATE CONSTRAINT hype_range;
        """))
    logger.info("Post-migration objects created and constraints validated.")


# ------------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------------
def init_db():
    try:
        # 1. Alembic first
        alembic_cfg = config.Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Alembic migrations complete.")

        # 2. ORM fallback
        create_missing_tables()

        # 3. Seed data
        seed_insight_types()

        # 4. Post-migration objects (view, partition, etc.)
        create_post_migration_objects()

    except SQLAlchemyError as e:
        logger.exception("Database bootstrap failed: %s", e)
        raise


if __name__ == "__main__":
    init_db()