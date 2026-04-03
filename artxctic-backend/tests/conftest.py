"""Test fixtures for the Artxtic backend test suite.

Uses the same artxtic_test database. Each test gets an independent
httpx AsyncClient that talks to the FastAPI app through ASGI transport.
"""

from __future__ import annotations

from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

# ── Test database URL ─────────────────────────────────────────
_base_url = settings.DATABASE_URL
if "artxtic" in _base_url and "artxtic_test" not in _base_url:
    TEST_DATABASE_URL = _base_url.replace("/artxtic", "/artxtic_test")
else:
    TEST_DATABASE_URL = _base_url + "_test"

if TEST_DATABASE_URL.startswith("postgresql://"):
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )


# ── Per-test engine + session ─────────────────────────────────

@pytest_asyncio.fixture
async def db_session():
    """Create tables, yield a session, rollback, then drop tables."""
    # Import all models so Base.metadata is populated
    from app.models.user import User  # noqa: F401
    from app.models.auth import (  # noqa: F401
        EmailVerificationToken,
        PasswordResetToken,
        RefreshToken,
    )
    from app.models.subscription import SubscriptionPlan, Subscription  # noqa: F401
    from app.models.media import Media  # noqa: F401
    from app.models.usage import UsageLimit  # noqa: F401
    from app.models.queue import GenerationJob  # noqa: F401
    from app.models.audit import AuditLog  # noqa: F401

    engine = create_async_engine(TEST_DATABASE_URL, echo=False, pool_pre_ping=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with factory() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP test client with DB dependency overridden."""

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def registered_user(db_session: AsyncSession):
    """Create and return a registered, verified test user."""
    from app.core.snowflake import generate_id
    from app.models.user import User
    import bcrypt

    hashed = bcrypt.hashpw(b"StrongPass1", bcrypt.gensalt(12)).decode("utf-8")

    user = User(
        id=generate_id(),
        email="test@example.com",
        name="Test User",
        password_hash=hashed,
        is_verified=True,
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, registered_user) -> AsyncClient:
    """Client pre-authenticated with an access token cookie."""
    from app.core.security import create_access_token

    token = create_access_token({"sub": str(registered_user.id)})
    client.cookies.set("access_token", token)
    return client
