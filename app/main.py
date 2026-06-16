from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.database import async_session, init_db, sync_database_sequences
from app.api.v1 import proyectos, experiencias, estudios, perfil, images, chat, frases, seccion_config, ai, storage_auth, og, cover_letters
from app.authentication.router import auth_router
from app.authentication.google_oauth_router import google_router
from app.authentication.user_details_router import user_details_router
from app.registration.router import account_router
from app.services.auth import seed_admin_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as session:
        await seed_admin_user(session)
        await session.commit()
    # Sincronizamos secuencialmente las secuencias de base de datos en PostgreSQL
    await sync_database_sequences()

    yield


app = FastAPI(
    title="Portafolio API - Jaime Campillay",
    description="API asíncrona para la gestión de trayectoria profesional",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(google_router, prefix="/api/v1")
app.include_router(user_details_router, prefix="/api/v1")
app.include_router(account_router, prefix="/api/v1/auth")
app.include_router(proyectos.router, prefix="/api/v1")
app.include_router(experiencias.router, prefix="/api/v1")
app.include_router(estudios.router, prefix="/api/v1")
app.include_router(perfil.router, prefix="/api/v1")
app.include_router(images.router, prefix="/api/v1/images")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(frases.router, prefix="/api/v1")
app.include_router(seccion_config.router, prefix="/api/v1/seccion_config", tags=["seccion_config"])
app.include_router(ai.router, prefix="/api/v1")
app.include_router(storage_auth.router, prefix="/api/v1")
app.include_router(cover_letters.router, prefix="/api/v1")
app.include_router(og.router)



@app.get("/health")
async def health():
    return {"status": "ok"}
