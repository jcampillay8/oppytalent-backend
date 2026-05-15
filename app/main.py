from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import async_session, init_db
from app.api.v1 import auth, proyectos, experiencias, estudios, perfil, images
from app.services.auth import seed_admin_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as session:
        await seed_admin_user(session)
        await session.commit()
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

app.include_router(auth.router, prefix="/api/v1")
app.include_router(proyectos.router, prefix="/api/v1")
app.include_router(experiencias.router, prefix="/api/v1")
app.include_router(estudios.router, prefix="/api/v1")
app.include_router(perfil.router, prefix="/api/v1")
app.include_router(images.router, prefix="/api/v1/images")


@app.get("/health")
async def health():
    return {"status": "ok"}
