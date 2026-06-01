"""Merge heads and add fields

Revision ID: b3a7c8d9e0f1
Revises: 476182ea2253, 48f69cfcf581
Create Date: 2026-06-01 16:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b3a7c8d9e0f1'
down_revision: Union[str, Sequence[str], None] = ('476182ea2253', '48f69cfcf581')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Check perfiles columns
    perfiles_cols = [col['name'] for col in inspector.get_columns('perfiles')]
    if 'youtube_url' not in perfiles_cols:
        op.add_column('perfiles', sa.Column('youtube_url', sa.String(length=500), nullable=True))
    if 'certificaciones' not in perfiles_cols:
        op.add_column('perfiles', sa.Column('certificaciones', sa.JSON(), nullable=False, server_default='[]'))
    if 'idiomas' not in perfiles_cols:
        op.add_column('perfiles', sa.Column('idiomas', sa.JSON(), nullable=False, server_default='[]'))
        
    # Check proyectos columns
    proyectos_cols = [col['name'] for col in inspector.get_columns('proyectos')]
    if 'youtube_url' not in proyectos_cols:
        op.add_column('proyectos', sa.Column('youtube_url', sa.String(length=500), nullable=True))

def downgrade() -> None:
    op.drop_column('perfiles', 'youtube_url')
    op.drop_column('perfiles', 'certificaciones')
    op.drop_column('perfiles', 'idiomas')
    op.drop_column('proyectos', 'youtube_url')
