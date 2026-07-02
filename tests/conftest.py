import os
os.environ["ENVIRONMENT"] = "test"
import pytest
import pytest_asyncio
import uuid
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import get_db, Base, init_db
from app.config import settings
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.models.rbac import Role, Permission, RolePermission

TEST_DB_URL = settings.database_url.rsplit("/", 1)[0] + "/oppytalent_test"

test_engine = create_async_engine(
    TEST_DB_URL,
    echo=False,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://test",
        timeout=30.0,
    ) as client:
        yield client


@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def seed_roles(async_client):
    async with TestingSessionLocal() as session:
        existing = await session.execute(__import__("sqlalchemy").select(Role).where(Role.name == "Talent"))
        if existing.scalar_one_or_none():
            return

        perms = [
            Permission(codename="can_edit_portfolio", name="Edit Portfolio"),
            Permission(codename="can_view_own_feedback", name="View Own Feedback"),
            Permission(codename="can_view_demand", name="View Market Demand"),
            Permission(codename="can_execute_tribunal", name="Execute B2B Tribunal"),
            Permission(codename="can_use_b2b_search", name="Use B2B Search"),
            Permission(codename="can_impersonate", name="Impersonate Roles"),
            Permission(codename="can_approve_kyc", name="Approve KYC"),
            Permission(codename="can_manage_roles", name="Manage Roles"),
        ]
        session.add_all(perms)
        await session.flush()

        perm_map = {p.codename: p for p in perms}

        roles_data = {
            "Owner": ["can_edit_portfolio", "can_view_own_feedback", "can_view_demand",
                      "can_execute_tribunal", "can_use_b2b_search", "can_impersonate",
                      "can_approve_kyc", "can_manage_roles"],
            "Admin": ["can_approve_kyc", "can_view_demand"],
            "Worker": ["can_view_demand"],
            "Hunter": ["can_execute_tribunal", "can_use_b2b_search", "can_view_demand"],
            "Talent": ["can_edit_portfolio", "can_view_own_feedback", "can_view_demand"],
        }

        for role_name, role_perms in roles_data.items():
            role = Role(name=role_name, description=role_name)
            session.add(role)
            await session.flush()
            for codename in role_perms:
                session.add(RolePermission(role_id=role.id, permission_id=perm_map[codename].id))

        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def test_user(seed_roles, async_client):
    from app.utils import get_hashed_password

    async with TestingSessionLocal() as session:
        existing = await session.execute(
            __import__("sqlalchemy").select(Usuario).where(Usuario.email == "testuser@oppytalent.com")
        )
        user = existing.scalar_one_or_none()
        if user:
            return user

        role_result = await session.execute(
            __import__("sqlalchemy").select(Role).where(Role.name == "Talent")
        )
        talent_role = role_result.scalar_one_or_none()

        user = Usuario(
            id=uuid.uuid4(),
            username="testuser",
            email="testuser@oppytalent.com",
            hashed_password=await get_hashed_password("TestPass123!"),
            first_name="Test",
            last_name="User",
            role="VIEWER",
            role_id=talent_role.id if talent_role else None,
            has_accepted_terms=True,
            freemium_tier="BASIC",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture(scope="session")
async def test_admin_user(seed_roles, async_client):
    from app.utils import get_hashed_password

    async with TestingSessionLocal() as session:
        existing = await session.execute(
            __import__("sqlalchemy").select(Usuario).where(Usuario.email == "admin@oppytalent.com")
        )
        user = existing.scalar_one_or_none()
        if user:
            return user

        role_result = await session.execute(
            __import__("sqlalchemy").select(Role).where(Role.name == "Owner")
        )
        owner_role = role_result.scalar_one_or_none()

        user = Usuario(
            id=uuid.uuid4(),
            username="testadmin",
            email="admin@oppytalent.com",
            hashed_password=await get_hashed_password("AdminPass123!"),
            first_name="Admin",
            last_name="User",
            role="ADMIN",
            role_id=owner_role.id if owner_role else None,
            has_accepted_terms=True,
            freemium_tier="ADMIN",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture(scope="session")
async def auth_client(test_user):
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://test",
        timeout=30.0,
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser@oppytalent.com",
                "password": "TestPass123!",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        login_data = response.json()
        token = login_data.get("access_token") or login_data.get("accessToken")
        if token:
            client.headers.update({"Authorization": f"Bearer {token}"})
        yield client


@pytest_asyncio.fixture(scope="session")
async def admin_auth_client(test_admin_user):
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://test",
        timeout=30.0,
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@oppytalent.com",
                "password": "AdminPass123!",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        login_data = response.json()
        token = login_data.get("access_token") or login_data.get("accessToken")
        if token:
            client.headers.update({"Authorization": f"Bearer {token}"})
        yield client
