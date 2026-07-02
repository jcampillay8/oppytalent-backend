import uuid
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from jose import jwt
from sqlalchemy import text

from src.config import settings
from src.main import app
from src.database import async_session_maker
from src.tenant_management.models import Holding, LegalEntity, Tenant, AppModule, IndustryVertical, BusinessType
from src.models import User
from src.utils import get_hashed_password


ADMIN_EMAIL = "superadmin@oppytest.test"
ADMIN_PASSWORD = "SuperAdminPass123!"
ADMIN_USERNAME = "superadmin"


@pytest_asyncio.fixture(scope="session")
async def admin_test_data():
    """
    Crea los registros mínimos en la BD de pruebas para que los tests
    administrativos funcionen: Holding → LegalEntity → Tenant + Superuser.
    Retorna un dict con los IDs creados y un JWT de superadmin.
    """
    data = {}

    async with async_session_maker() as session:
        from sqlalchemy import select
        
        # 1. Holding
        holding = (await session.execute(select(Holding).where(Holding.nombre == "Admin Test Holding"))).scalar_one_or_none()
        if not holding:
            holding = Holding(id=uuid.uuid4(), nombre="Admin Test Holding", is_active=True)
            session.add(holding)
            await session.commit()
            await session.refresh(holding)
            
        # 2. LegalEntity
        le = (await session.execute(select(LegalEntity).where(LegalEntity.legal_name == "Admin Test Legal Entity"))).scalar_one_or_none()
        if not le:
            le = LegalEntity(
                id=uuid.uuid4(),
                holding_id=holding.id,
                tax_id="76.123.456-7",
                legal_name="Admin Test Legal Entity",
                is_active=True,
            )
            session.add(le)
            await session.commit()
            await session.refresh(le)
            
        # 3. Tenant
        tenant = (await session.execute(select(Tenant).where(Tenant.slug == "admin-test-tenant"))).scalar_one_or_none()
        if not tenant:
            tenant = Tenant(
                id=uuid.uuid4(),
                schema_name="admin_test_schema",
                nombre_comercial="Admin Test Tenant",
                slug="admin-test-tenant",
                is_active=True,
                legal_entity_id=le.id,
            )
            session.add(tenant)
            await session.commit()
            await session.refresh(tenant)
            
        # 4. User
        admin_user = (await session.execute(select(User).where(User.email == ADMIN_EMAIL))).scalar_one_or_none()
        if not admin_user:
            hashed = await get_hashed_password(ADMIN_PASSWORD)
            admin_user = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=hashed,
                first_name="Super",
                last_name="Admin",
                is_superuser=True,
            )
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)
            
        holding_id = holding.id
        le_id = le.id
        tenant_id = tenant.id


        data["holding_id"] = holding_id
        data["legal_entity_id"] = le_id
        data["tenant_id"] = tenant_id
        data["admin_user_id"] = admin_user.id

    # 5. Create JWT token for superadmin
    token = jwt.encode(
        {
            "sub": ADMIN_EMAIL,
            "schema_name": settings.DB_SCHEMA,
            "exp": datetime.now(timezone.utc) + timedelta(hours=2),
            "iat": datetime.now(timezone.utc),
        },
        settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.ENCRYPTION_ALGORITHM,
    )
    data["admin_token"] = token

    return data


@pytest_asyncio.fixture(scope="session")
async def admin_headers(admin_test_data):
    """Retorna headers HTTP con autenticación de superadmin."""
    token = admin_test_data["admin_token"]
    return {
        "Authorization": f"Bearer {token}",
        "X-Tenant-Schema": settings.DB_SCHEMA,
    }


@pytest_asyncio.fixture(scope="session")
async def admin_client(admin_headers):
    """Retorna un AsyncClient con headers de superadmin preconfigurados."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        timeout=30.0,
    ) as client:
        client.headers.update(admin_headers)
        yield client


@pytest_asyncio.fixture(scope="session")
async def industry_vertical(admin_test_data):
    """Crea una IndustryVertical para tests de BusinessType."""
    async with async_session_maker() as session:
        iv = IndustryVertical(
            id=uuid.uuid4(),
            nombre="Test Vertical ISO",
            descripcion="Vertical for ISO testing",
            is_active=True,
        )
        session.add(iv)
        await session.commit()
        await session.refresh(iv)
        return {"id": iv.id, "nombre": iv.nombre}


@pytest_asyncio.fixture(scope="session")
async def app_module(admin_test_data):
    """Crea un AppModule para tests de módulos SaaS."""
    async with async_session_maker() as session:
        mod = AppModule(
            id=uuid.uuid4(),
            code="test_module_iso",
            name="Test Module ISO",
            description="Module for ISO testing",
            is_active=True,
        )
        session.add(mod)
        await session.commit()
        await session.refresh(mod)
        return {"id": mod.id, "code": mod.code, "name": mod.name}
