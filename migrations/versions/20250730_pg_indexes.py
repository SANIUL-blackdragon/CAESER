"""Add PostgreSQL indexes for categories, predictions, social_data  
   + partitioning, view, constraints (post-upgrade)

Revision ID: 20250730_pg_indexes
Revises: a9772e6a7448
Create Date: 2025-07-30 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "20250730_pg_indexes"
down_revision = "a9772e6a7448"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Original indexes
    op.create_index("idx_categories_name", "categories", ["category_name"])
    op.create_index("idx_predictions_product", "predictions", ["product_name"])
    op.create_index("idx_social_data_source", "social_data", ["source"])
    op.create_index(
        "idx_social_data_source_timestamp",
        "social_data",
        ["source", "timestamp"]
    )

    # 2. NEW: index on text column for faster text filtering
    op.create_index("idx_social_data_text", "social_data", ["text"])

    # 3. Partition social_data by year (2025 and 2026)
    op.execute("""
        ALTER TABLE social_data
        PARTITION BY RANGE (timestamp);
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS social_data_2025
        PARTITION OF social_data
        FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS social_data_2026
        PARTITION OF social_data
        FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
    """)

    # 4. Complex view
    op.execute("""
        CREATE OR REPLACE VIEW avg_hype_per_category AS
        SELECT category, AVG(predicted_uplift) AS avg_hype
        FROM predictions
        GROUP BY category;
    """)

    # 5. Integrity constraint on competitors
    op.add_column("competitors", sa.Column("hype_score", sa.Float))
    op.execute("""
        ALTER TABLE competitors
        ADD CONSTRAINT hype_range
        CHECK (hype_score >= 0 AND hype_score <= 100)
        NOT VALID;   -- allows existing rows to be fixed first
    """)


def downgrade() -> None:
    # 5. Reverse constraints
    op.drop_constraint("hype_range", "competitors")
    op.drop_column("competitors", "hype_score")

    # 4. Reverse view
    op.execute("DROP VIEW IF EXISTS avg_hype_per_category")

    # 3. Reverse partitioning
    op.execute("DROP TABLE IF EXISTS social_data_2026")
    op.execute("DROP TABLE IF EXISTS social_data_2025")
    op.execute("ALTER TABLE social_data DETACH PARTITION social_data_2025")
    op.execute("ALTER TABLE social_data DETACH PARTITION social_data_2026")
    op.execute("ALTER TABLE social_data SET NOT PARTITIONED;")

    # 2. NEW: drop text index
    op.drop_index("idx_social_data_text", table_name="social_data")

    # 1. Reverse original indexes
    op.drop_index("idx_social_data_source_timestamp", table_name="social_data")
    op.drop_index("idx_social_data_source", table_name="social_data")
    op.drop_index("idx_predictions_product", table_name="predictions")
    op.drop_index("idx_categories_name", table_name="categories")