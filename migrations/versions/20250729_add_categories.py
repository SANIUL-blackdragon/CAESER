"""Add flexible categories table

Revision ID: 20250729_add_categories
Revises: 4c0ff554c6e2
Create Date: 2025-07-29 08:00:00

"""
from alembic import op
import sqlalchemy as sa

revision = "20250729_add_categories"
down_revision = "4c0ff554c6e2"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category_name", sa.String(), nullable=False, unique=True),
        sa.Column("keywords", sa.Text(), nullable=False)  # comma-separated
    )

def downgrade() -> None:
    op.drop_table("categories")