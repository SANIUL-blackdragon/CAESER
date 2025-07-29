"""Add competitors table

Revision ID: 20250729_add_competitors
Revises: 4c0ff554c6e2
Create Date: 2025-07-29 08:05:00
"""
from alembic import op
import sqlalchemy as sa

revision = "20250729_add_competitors"
down_revision = "4c0ff554c6e2"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "competitors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("hype_score", sa.Float, nullable=False, default=0.0)
    )

def downgrade() -> None:
    op.drop_table("competitors")