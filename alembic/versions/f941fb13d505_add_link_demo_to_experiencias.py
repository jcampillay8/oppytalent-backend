"""add link_demo to experiencias

Revision ID: f941fb13d505
Revises: 5ff2a59378b5
Create Date: 2026-05-20 09:15:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f941fb13d505'
down_revision: Union[str, None] = '5ff2a59378b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('experiencias', sa.Column('link_demo', sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column('experiencias', 'link_demo')
