"""Create all core tables

Revision ID: 0001
Revises:
Create Date: 2026-05-13
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.Text(), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="VIEWER"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_usuarios_id"), "usuarios", ["id"])
    op.create_index(op.f("ix_usuarios_username"), "usuarios", ["username"], unique=True)

    op.create_table(
        "proyectos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("titulo", sa.String(255), nullable=False),
        sa.Column("descripcion_corta", sa.String(500), nullable=False),
        sa.Column("descripcion_detallada", sa.Text(), nullable=False),
        sa.Column("stack_tecnologico", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("fecha_proyecto", sa.Date(), nullable=False),
        sa.Column("link_github", sa.String(500), nullable=True),
        sa.Column("link_demo", sa.String(500), nullable=True),
        sa.Column("kpis", sa.JSON(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_proyectos_id"), "proyectos", ["id"])

    op.create_table(
        "experiencias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("empresa", sa.String(255), nullable=False),
        sa.Column("rol", sa.String(255), nullable=False),
        sa.Column("periodo_inicio", sa.Date(), nullable=False),
        sa.Column("periodo_fin", sa.Date(), nullable=True),
        sa.Column("descripcion_logros", sa.Text(), nullable=False),
        sa.Column("tags_industria", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_experiencias_id"), "experiencias", ["id"])

    op.create_table(
        "estudios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("institucion", sa.String(255), nullable=False),
        sa.Column("titulo", sa.String(255), nullable=False),
        sa.Column("anio_obtencion", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_estudios_id"), "estudios", ["id"])


def downgrade() -> None:
    op.drop_table("estudios")
    op.drop_table("experiencias")
    op.drop_table("proyectos")
    op.drop_table("usuarios")
