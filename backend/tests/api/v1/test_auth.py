import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import user as user_crud
from app.schemas.user import UserCreate

pytestmark = pytest.mark.asyncio

async def test_register_user(client: AsyncClient):
    login = "testuser@example.com"
    password = "a_strong_password"
    response = await client.post(
        f"{settings.API_V1_STR}/users/register",
        json={"login": login, "password": password},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["login"] == login
    assert "id" in data
    assert "hashed_password" not in data

async def test_register_existing_user(client: AsyncClient, test_user: User):
    password = "a_strong_password"
    response = await client.post(
        f"{settings.API_V1_STR}/users/register",
        json={"login": test_user.login, "password": password},
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

async def test_get_access_token(client: AsyncClient, db_session: AsyncSession):
    login = "get.token.user@example.com"
    password = "testpassword123"
    user_in = UserCreate(login=login, password=password)
    await user_crud.create(db_session, obj_in=user_in)

    response = await client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": login, "password": password},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

async def test_get_access_token_wrong_password(client: AsyncClient, test_user: User):
    response = await client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": test_user.login, "password": "wrong_password"},
    )
    assert response.status_code == 401
    assert "Incorrect login or password" in response.json()["detail"]

async def test_get_me(authenticated_client: AsyncClient, test_user: User):
    response = await authenticated_client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["login"] == test_user.login