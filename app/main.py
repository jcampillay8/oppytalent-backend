import sys
import traceback
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.database import async_session, init_db, sync_database_sequences
from app.api.v1 import proyectos, experiencias, estudios, perfil, images, chat, frases, seccion_config, ai, storage_auth, og, reconocimientos, habilitaciones, b2b, admin_rbac, chat_p2p, network, freemium
from app.authentication.router import auth_router
from app.authentication.google_oauth_router import google_router
from app.authentication.user_details_router import user_details_router
from app.registration.router import account_router
from app.services.auth import seed_admin_user
from app.scripts.seed_rbac import seed_rbac
from app.scripts.seed_ai import seed_ai_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    
    # 0. Automate AI Models seeding
    await seed_ai_models()
    
    # 1. Automate RBAC Seeding on every startup
    await seed_rbac()
    
    # 2. Ensure Admin user exists
    async with async_session() as session:
        await seed_admin_user(session)
        await session.commit()
        
    # 3. Sincronizamos secuencialmente las secuencias de base de datos en PostgreSQL
    await sync_database_sequences()

    yield


current_env = settings.ENVIRONMENT.lower()

is_production = current_env == "production"
is_test = current_env == "test"
is_development = current_env == "development"

# Solo ocultamos la documentación si estamos en producción.
show_docs = not is_production

app = FastAPI(
    title="Portafolio API - OppyTalent",
    description="API asíncrona para la gestión de talento y reclutamiento B2B",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if show_docs else None,
    redoc_url="/redoc" if show_docs else None,
    openapi_url="/openapi.json" if show_docs else None
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print("GLOBAL EXCEPTION:", traceback.format_exc(), file=sys.stderr)
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

# Reglas de Seguridad CORS por ambiente
if is_production:
    cors_origins = [
        "https://oppytalent-frontend-production.up.railway.app",
        "https://www.oppytalent.com",
        "https://oppytalent.com",
        settings.WEBSITE_URL
    ]
elif is_test:
    cors_origins = ["http://localhost:5173", settings.WEBSITE_URL] # Híbrido para QA
else:
    cors_origins = ["*"] # Totalmente abierto para Desarrollo local

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if "server" in response.headers:
            del response.headers["server"]
        return response

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if is_production and request.headers.get("x-forwarded-proto") == "https":
            request.scope["scheme"] = "https"
        response = await call_next(request)
        return response

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(google_router, prefix="/api/v1")
app.include_router(user_details_router, prefix="/api/v1")
app.include_router(account_router, prefix="/api/v1/auth")
app.include_router(proyectos.router, prefix="/api/v1")
app.include_router(experiencias.router, prefix="/api/v1")
app.include_router(estudios.router, prefix="/api/v1")
app.include_router(perfil.router, prefix="/api/v1")
app.include_router(reconocimientos.router, prefix="/api/v1")
app.include_router(habilitaciones.router, prefix="/api/v1")
app.include_router(images.router, prefix="/api/v1/images")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(chat_p2p.router, prefix="/api/v1/chat-p2p")
app.include_router(frases.router, prefix="/api/v1")
app.include_router(seccion_config.router, prefix="/api/v1/seccion_config", tags=["seccion_config"])
app.include_router(ai.router, prefix="/api/v1")
app.include_router(storage_auth.router, prefix="/api/v1")
app.include_router(b2b.router, prefix="/api/v1")
app.include_router(admin_rbac.router, prefix="/api/v1")
app.include_router(network.router, prefix="/api/v1")
app.include_router(freemium.router, prefix="/api/v1")
app.include_router(og.router)



@app.get("/health")
@limiter.limit("5/minute")
async def health(request: Request):
    return {"status": "ok"}
