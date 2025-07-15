import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.api.v1.deps import get_db_session
from app.models import User
from tests.utils.user import create_random_user, user_authentication_headers

# Создаем асинхронный движок для тестовой БД
test_engine = create_async_engine(str(settings.ASYNC_DATABASE_URI), echo=False)
TestingSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create test database tables before tests run, and drop them after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a test function."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback() # Rollback changes after test

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Fixture to get an httpx.AsyncClient."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    del app.dependency_overrides[get_db_session]

@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """Fixture to create a regular test user."""
    return await create_random_user(db_session)

@pytest.fixture(scope="function")
async def test_admin_user(db_session: AsyncSession) -> User:
    """Fixture to create an admin test user."""
    return await create_random_user(db_session, is_admin=True)

@pytest.fixture(scope="function")
def auth_headers(test_user: User) -> dict[str, str]:
    """Fixture to get authentication headers for a regular user."""
    return user_authentication_headers(login=test_user.login)

@pytest.fixture(scope="function")
def admin_auth_headers(test_admin_user: User) -> dict[str, str]:
    """Fixture to get authentication headers for an admin user."""
    return user_authentication_headers(login=test_admin_user.login)