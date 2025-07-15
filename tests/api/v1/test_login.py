import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.schemas.user import UserCreate
from app.crud.user import user as user_crud

pytestmark = pytest.mark.asyncio

async def test_register_user(client: AsyncClient, db_session: AsyncSession):
    login = "testuser@example.com"
    password = "testpassword"
    response = await client.post(
        f"{settings.API_V1_STR}/users/register",
        json={"login": login, "password": password},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["login"] == login
    assert "id" in data
    assert "hashed_password" not in data

async def test_get_access_token(client: AsyncClient, test_user: User):
    login = test_user.login
    password = "password" # Default password used in user creation utils
    
    # We need to create a user with a known password
    user_in = UserCreate(login="get.token.user", password=password)
    await user_crud.create(client.app.dependency_overrides[get_db_session](), obj_in=user_in)

    response = await client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": user_in.login, "password": password},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

async def test_get_me(client: AsyncClient, auth_headers: dict):
    response = await client.get(f"{settings.API_V1_STR}/users/me", headers=auth_headers)
    assert response.status_code == 200
    user_data = response.json()
    assert "login" in user_data
    assert user_data["login"] is not None