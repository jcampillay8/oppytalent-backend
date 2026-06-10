import json
import os
from datetime import datetime, date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.perfil import Perfil
from app.models.proyecto import Proyecto
from app.models.experiencia import Experiencia
from app.models.estudio import Estudio
from app.models.usuario import Usuario

JSON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "json_data")


def _serialize(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj


def _model_to_dict(entity):
    data = {}
    for column in entity.__table__.columns:
        val = getattr(entity, column.name)
        data[column.name] = _serialize(val)
    return data


async def sync_all_json(db: AsyncSession | None = None):
    models = {
        "perfil": Perfil,
        "proyectos": Proyecto,
        "experiencias": Experiencia,
        "estudios": Estudio,
        "usuarios": Usuario,
    }

    if db:
        await _sync_with_session(db, models)
    else:
        async with async_session() as session:
            await _sync_with_session(session, models)


async def _sync_with_session(db: AsyncSession, models: dict):
    os.makedirs(JSON_DIR, exist_ok=True)
    for filename, model in models.items():
        result = await db.execute(select(model).where(model.is_active == True))
        rows = result.scalars().all()
        data = [_model_to_dict(r) for r in rows]

        filepath = os.path.join(JSON_DIR, f"{filename}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def load_json_context() -> str:
    sections = []
    for filename in ["perfil.json", "experiencias.json", "proyectos.json", "estudios.json"]:
        filepath = os.path.join(JSON_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            sections.append(f"=== {filename.replace('.json', '').upper()} ===\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    return "\n\n".join(sections)
