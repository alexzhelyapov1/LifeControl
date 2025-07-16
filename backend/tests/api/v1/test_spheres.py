import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.sphere import sphere as sphere_crud
from app.models import User
from app.schemas.sphere import SphereCreate
from tests.utils.user import create_random_user, user_authentication_headers

pytestmark = pytest.mark.asyncio

async def test_create_read_update_delete_sphere(authenticated_client: AsyncClient, db_session, test_user: User):
    # 1. CREATE
    sphere_data = {"name": "Test Sphere", "description": "My test sphere"}
    response = await authenticated_client.post(f"{settings.API_V1_STR}/spheres/", json=sphere_data)
    assert response.status_code == 201
    created_sphere = response.json()
    sphere_id = created_sphere["id"]
    assert created_sphere["name"] == sphere_data["name"]
    assert created_sphere["owner"]["id"] == test_user.id

    # 2. READ ONE
    response = await authenticated_client.get(f"{settings.API_V1_STR}/spheres/{sphere_id}")
    assert response.status_code == 200
    read_sphere = response.json()
    assert read_sphere["name"] == sphere_data["name"]

    # 3. READ ALL
    response = await authenticated_client.get(f"{settings.API_V1_STR}/spheres/")
    assert response.status_code == 200
    assert any(s["id"] == sphere_id for s in response.json())

    # 4. UPDATE
    update_data = {"name": "Updated Sphere Name"}
    response = await authenticated_client.put(f"{settings.API_V1_STR}/spheres/{sphere_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

    # 5. DELETE
    response = await authenticated_client.delete(f"{settings.API_V1_STR}/spheres/{sphere_id}")
    assert response.status_code == 204

    # VERIFY DELETE
    response = await authenticated_client.get(f"{settings.API_V1_STR}/spheres/{sphere_id}")
    assert response.status_code == 404

# --- SCENARIO: VALIDATION ERROR (422) ---
@pytest.mark.parametrize("invalid_data", [
    {"name": ""}, # Empty name
    {"name": "a" * 101}, # Too long name
])
async def test_create_sphere_validation_error(authenticated_client: AsyncClient, invalid_data: dict):
    response = await authenticated_client.post(f"{settings.API_V1_STR}/spheres/", json=invalid_data)
    assert response.status_code == 422

# --- SCENARIO: UNAUTHORIZED (401) ---
async def test_read_sphere_unauthorized(client: AsyncClient):
    response = await client.get(f"{settings.API_V1_STR}/spheres/999")
    assert response.status_code == 401

# --- SCENARIO: PERMISSION DENIED (403/404) ---
async def test_access_other_user_sphere_permission_denied(
    client: AsyncClient, db_session: AsyncSession, test_user: User
):
    # User 1 creates a sphere
    sphere = await sphere_crud.create_with_owner(
        db_session, obj_in=SphereCreate(name="User1's Private Sphere"), owner_id=test_user.id
    )

    # User 2 is created
    user2 = await create_random_user(db_session)
    user2_headers = user_authentication_headers(login=user2.login)

    # User 2 tries to access User 1's sphere and fails
    response = await client.get(f"{settings.API_V1_STR}/spheres/{sphere.id}", headers=user2_headers)
    assert response.status_code == 403 # Forbidden

    # User 2 tries to update it and fails
    response = await client.put(f"{settings.API_V1_STR}/spheres/{sphere.id}", headers=user2_headers, json={"name": "hacked"})
    assert response.status_code == 403 # Forbidden

async def test_editor_can_edit_but_not_delete(client: AsyncClient, db_session: AsyncSession, test_user: User):
    # User 2 (editor) is created
    editor_user = await create_random_user(db_session)
    
    # User 1 creates a sphere and shares it with User 2 as an editor
    sphere_in = SphereCreate(name="Shared Sphere", editor_ids=[editor_user.id])
    sphere = await sphere_crud.create_with_owner(db_session, obj_in=sphere_in, owner_id=test_user.id)
    
    editor_headers = user_authentication_headers(login=editor_user.login)
    
    # Editor can READ the sphere
    response = await client.get(f"{settings.API_V1_STR}/spheres/{sphere.id}", headers=editor_headers)
    assert response.status_code == 200
    
    # Editor can UPDATE the sphere
    update_data = {"name": "Updated by Editor"}
    response = await client.put(f"{settings.API_V1_STR}/spheres/{sphere.id}", headers=editor_headers, json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

    # Editor CANNOT DELETE the sphere (our dependency is strict: only owner can delete)
    response = await client.delete(f"{settings.API_V1_STR}/spheres/{sphere.id}", headers=editor_headers)
    assert response.status_code == 403 # Forbidden