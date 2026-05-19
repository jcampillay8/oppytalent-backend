from datetime import datetime, timezone

from sqlalchemy import DateTime, Boolean, func, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def sync_database_sequences():
    """
    Sincroniza de forma dinámica las secuencias de las tablas de la base de datos en PostgreSQL.
    Esto soluciona el problema de "Duplicate key value violates unique constraint" provocado
    por la inserción manual de registros con IDs hardcodeados.
    """
    # Importamos los modelos dentro de la función para evitar importaciones circulares
    # y asegurar que todas las tablas estén registradas en Base.metadata
    from app.models import Usuario, Proyecto, Experiencia, Estudio, Perfil  # noqa: F401

    if engine.dialect.name != "postgresql":
        return

    async with engine.begin() as conn:
        for table_name, table in Base.metadata.tables.items():
            if "id" in table.columns:
                try:
                    # Obtenemos de manera segura el nombre de la secuencia en PostgreSQL
                    seq_query = text(f"SELECT pg_get_serial_sequence('{table_name}', 'id')")
                    result = await conn.execute(seq_query)
                    seq_name = result.scalar()

                    if seq_name:
                        # Sincronizamos la secuencia con el valor de ID máximo actual
                        # Si la tabla está vacía, se inicializa en 1 y se marca is_called como false.
                        # Si tiene registros, se ajusta al MAX(id) con is_called como true.
                        sync_query = text(f"""
                            SELECT setval(
                                '{seq_name}',
                                COALESCE((SELECT MAX(id) FROM {table_name}), 1),
                                COALESCE((SELECT MAX(id) FROM {table_name}) IS NOT NULL, false)
                            )
                        """)
                        await conn.execute(sync_query)
                except Exception as e:
                    # Registramos el error de forma segura pero no interrumpimos el flujo
                    import logging
                    logger = logging.getLogger("uvicorn.error")
                    logger.warning(f"No se pudo sincronizar la secuencia de la tabla {table_name}: {e}")
