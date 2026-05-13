"""Add image_url column to proyectos, experiencias, estudios

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-13
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("proyectos", sa.Column("image_url", sa.String(500), nullable=True))
    op.add_column("experiencias", sa.Column("image_url", sa.String(500), nullable=True))
    op.add_column("estudios", sa.Column("image_url", sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column("estudios", "image_url")
    op.drop_column("experiencias", "image_url")
    op.drop_column("proyectos", "image_url")
