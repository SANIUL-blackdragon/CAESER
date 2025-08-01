from alembic import op
import sqlalchemy as sa

revision = "20250730_pg_indexes"
down_revision = "a9772e6a7448"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create a new partitioned table
    op.execute("""
        CREATE TABLE social_data_new (
            id SERIAL,
            platform TEXT,
            post_content TEXT,
            sentiment_score REAL,
            created_at TIMESTAMPTZ,
            PRIMARY KEY (id, created_at)
        ) PARTITION BY RANGE (created_at);
    """)
    
    # Create partitions for 2025 and 2026
    op.execute("""
        CREATE TABLE social_data_2025 PARTITION OF social_data_new
        FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
    """)
    op.execute("""
        CREATE TABLE social_data_2026 PARTITION OF social_data_new
        FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
    """)
    
    # Copy data from the old table
    op.execute("""
        INSERT INTO social_data_new (id, platform, post_content, sentiment_score, created_at)
        SELECT id, platform, post_content, sentiment_score, created_at FROM social_data;
    """)
    
    # Drop the old table and rename the new one
    op.execute("DROP TABLE social_data;")
    op.execute("ALTER TABLE social_data_new RENAME TO social_data;")
    
    # Create indexes
    op.create_index("idx_categories_name", "categories", ["name"])
    op.create_index("idx_predictions_product", "predictions", ["product_name"])
    op.create_index("idx_social_data_platform", "social_data", ["platform"])
    op.create_index("idx_social_data_platform_created_at", "social_data", ["platform", "created_at"])
    op.create_index("idx_social_data_post_content", "social_data", ["post_content"])
    
    # Create view
    op.execute("""
        CREATE OR REPLACE VIEW avg_trend_per_category AS
        SELECT category_id, AVG(trend_score) AS avg_trend
        FROM predictions
        GROUP BY category_id;
    """)
    
    # Add hype_score column and constraint
    op.add_column("competitors", sa.Column("hype_score", sa.Float))
    op.execute("""
        ALTER TABLE competitors
        ADD CONSTRAINT hype_range
        CHECK (hype_score >= 0 AND hype_score <= 100)
        NOT VALID;
    """)

def downgrade() -> None:
    # Reverse constraints
    op.drop_constraint("hype_range", "competitors")
    op.drop_column("competitors", "hype_score")
    
    # Reverse view
    op.execute("DROP VIEW IF EXISTS avg_trend_per_category")
    
    # Reverse indexes
    op.drop_index("idx_social_data_post_content", table_name="social_data")
    op.drop_index("idx_social_data_platform_created_at", table_name="social_data")
    op.drop_index("idx_social_data_platform", table_name="social_data")
    op.drop_index("idx_predictions_product", table_name="predictions")
    op.drop_index("idx_categories_name", table_name="categories")
    
    # Recreate the original non-partitioned table
    op.execute("""
        CREATE TABLE social_data_old AS SELECT * FROM social_data;
    """)
    op.execute("DROP TABLE social_data;")
    op.execute("ALTER TABLE social_data_old RENAME TO social_data;")