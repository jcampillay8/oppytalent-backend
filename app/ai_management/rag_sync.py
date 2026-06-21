import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.database import async_session

from app.models import Perfil, Experiencia, Proyecto, Estudio, Reconocimiento, Habilitacion
from app.models.portfolio_document import PortfolioDocument
from app.ai_management.embeddings import generate_embedding
from app.services.crypto import decrypt_value

def _model_to_dict(entity):
    data = {}
    for column in entity.__table__.columns:
        val = getattr(entity, column.name)
        # Avoid complex serialization issues with dates
        data[column.name] = str(val) if val is not None else None
    return data

async def sync_user_rag_embeddings(db: AsyncSession, usuario_id: int, api_key: str = None):
    """
    Sincroniza la base de datos de un usuario hacia la tabla PortfolioDocument (RAG Vectorial).
    Optimizado: Compara el texto de cada registro con el de la base de datos. Si el texto no cambió, 
    salta la generación del vector para ahorrar tokens y tiempo.
    """
    # 1. Traer todos los documentos existentes del usuario
    query_docs = select(PortfolioDocument).where(PortfolioDocument.usuario_id == usuario_id)
    result_docs = await db.execute(query_docs)
    existing_docs = result_docs.scalars().all()
    
    # Mapeo: (tipo_entidad, entidad_id) -> PortfolioDocument
    docs_map = {(d.tipo_entidad, d.entidad_id): d for d in existing_docs}
    
    models_mapping = {
        "PERFIL": Perfil,
        "EXPERIENCIA": Experiencia,
        "PROYECTO": Proyecto,
        "ESTUDIO": Estudio,
        "RECONOCIMIENTO": Reconocimiento,
        "HABILITACION": Habilitacion
    }
    
    upserted_count = 0
    docs_to_insert = []
    processed_keys = set()
    
    # 2. Iterar sobre todos los datos activos del usuario
    for tipo_entidad, model in models_mapping.items():
        query = select(model).where(model.is_active == True, model.usuario_id == usuario_id)
        result = await db.execute(query)
        rows = result.scalars().all()
        
        for row in rows:
            data = _model_to_dict(row)
            texto_representativo = f"Categoría: {tipo_entidad}\n"
            texto_representativo += json.dumps(data, indent=2, ensure_ascii=False)
            
            key = (tipo_entidad, row.id)
            processed_keys.add(key)
            
            existing_doc = docs_map.get(key)
            
            # Si existe y el texto es idéntico, ¡NO hacemos nada! (Ahorro de tokens)
            if existing_doc and existing_doc.contenido_texto == texto_representativo:
                continue
                
            # Si no existe, o el texto cambió, generamos el vector
            try:
                embedding = generate_embedding(texto_representativo, api_key=api_key)
                
                if existing_doc:
                    # Update
                    existing_doc.contenido_texto = texto_representativo
                    existing_doc.embedding = embedding
                    upserted_count += 1
                else:
                    # Insert
                    doc = PortfolioDocument(
                        usuario_id=usuario_id,
                        tipo_entidad=tipo_entidad,
                        entidad_id=row.id,
                        contenido_texto=texto_representativo,
                        embedding=embedding
                    )
                    docs_to_insert.append(doc)
                    upserted_count += 1
            except Exception as e:
                print(f"Error generando embedding para {tipo_entidad} ID {row.id}: {e}")
                
    if docs_to_insert:
        db.add_all(docs_to_insert)
        
    # 3. Eliminar los documentos que ya no existen en la DB (o que pasaron a is_active=False)
    keys_to_delete = set(docs_map.keys()) - processed_keys
    for key in keys_to_delete:
        doc_to_del = docs_map[key]
        await db.delete(doc_to_del)
    
    await db.commit()
    return upserted_count


async def _run_sync_in_background(usuario_id: int):
    async with async_session() as session:
        try:
            from app.models.usuario import Usuario
            user = await session.get(Usuario, usuario_id)
            if not user:
                return

            api_key = None
            if getattr(user, 'encrypted_gemini_key', None):
                try:
                    api_key = decrypt_value(user.encrypted_gemini_key)
                except Exception:
                    pass
                    
            await sync_user_rag_embeddings(session, usuario_id, api_key=api_key)
        except Exception as e:
            print(f"Error en sync background RAG: {e}")

def trigger_rag_sync_background(background_tasks, usuario_id: int):
    """
    Dispara la sincronización RAG en segundo plano sin bloquear la respuesta de la API.
    """
    background_tasks.add_task(_run_sync_in_background, usuario_id)
