"""merge categories and competitors

Revision ID: a9772e6a7448
Revises: 20250729_add_categories, 20250729_add_competitors
Create Date: 2025-07-29 17:25:26.581468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9772e6a7448'
down_revision: Union[str, Sequence[str], None] = ('20250729_add_categories', '20250729_add_competitors')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
