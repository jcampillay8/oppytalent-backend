import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.database import Base
from app.models import Usuario, Proyecto, Experiencia, Estudio, Perfil  # noqa: F401

async def test_neon_sync():
    url = "postgresql+asyncpg://neondb_owner:npg_ieMtaqTk74wg@ep-crimson-paper-acrdi7fw-pooler.sa-east-1.aws.neon.tech/portafolio?ssl=require"
    print(f"Connecting to: {url}")
    engine = create_async_engine(url, echo=True)
    
    async with engine.begin() as conn:
        print("Iterating over tables...")
        for table_name, table in Base.metadata.tables.items():
            if "id" in table.columns:
                print(f"Syncing table: {table_name}")
                try:
                    # Obtenemos de manera segura el nombre de la secuencia en PostgreSQL
                    seq_query = text(f"SELECT pg_get_serial_sequence('{table_name}', 'id')")
                    result = await conn.execute(seq_query)
                    seq_name = result.scalar()
                    print(f" -> Sequence name: {seq_name}")

                    if seq_name:
                        # Sincronizamos la secuencia
                        sync_query = text(f"""
                            SELECT setval(
                                '{seq_name}',
                                COALESCE((SELECT MAX(id) FROM {table_name}), 1),
                                COALESCE((SELECT MAX(id) FROM {table_name}) IS NOT NULL, false)
                            )
                        """)
                        sync_res = await conn.execute(sync_query)
                        print(f" -> Synchronized to: {sync_res.scalar()}")
                    else:
                        print(" -> No sequence associated with this table.")
                except Exception as e:
                    print(f" -> ERROR syncing table {table_name}: {e}")

asyncio.run(test_neon_sync())
