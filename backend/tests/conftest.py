import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api.v1.deps import get_db_session
from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.models import User
from tests.utils.user import create_random_user, user_authentication_headers

# Создаем асинхронный движок для тестовой БД.
# Он будет использовать переменные окружения, переданные Docker'ом для тестов.
test_engine = create_async_engine(str(settings.ASYNC_DATABASE_URI), echo=False)
TestingSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)

# Переопределяем зависимость get_db_session на время тестов,
# чтобы использовать сессию к тестовой БД.
async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db_session] = override_get_db_session

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    # Этот код теперь выполняется внутри Docker-контейнера `api_test`.
    # Миграции уже применены командой в docker-compose.test.yml.
    # Поэтому создание и удаление таблиц здесь больше не требуется.
    yield

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет транзакционную сессию для каждого теста."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для получения анонимного httpx.AsyncClient."""
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """Фикстура для создания обычного тестового пользователя."""
    return await create_random_user(db_session)

@pytest.fixture(scope="function")
def auth_headers(test_user: User) -> dict[str, str]:
    """Фикстура для получения заголовков аутентификации для обычного пользователя."""
    return user_authentication_headers(login=test_user.login)

@pytest.fixture
async def authenticated_client(client: AsyncClient, auth_headers: dict) -> AsyncClient:
    """Фикстура, предоставляющая AsyncClient с уже установленным заголовком авторизации."""
    client.headers.update(auth_headers)
    yield client