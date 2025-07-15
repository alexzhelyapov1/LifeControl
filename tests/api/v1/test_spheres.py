import pytest
from httpx import AsyncClient
from app.core.config import settings

pytestmark = pytest.mark.asyncio

async def test_create_and_read_sphere(client: AsyncClient, auth_headers: dict):
    # Create
    sphere_data = {"name": "Test Sphere", "description": "My test sphere"}
    response = await client.post(
        f"{settings.API_V1_STR}/spheres/",
        json=sphere_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    created_sphere = response.json()
    assert created_sphere["name"] == sphere_data["name"]
    assert "id" in created_sphere
    sphere_id = created_sphere["id"]

    # Read one
    response = await client.get(
        f"{settings.API_V1_STR}/spheres/{sphere_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    read_sphere = response.json()
    assert read_sphere["name"] == sphere_data["name"]

    # Read all
    response = await client.get(f"{settings.API_V1_STR}/spheres/", headers=auth_headers)
    assert response.status_code == 200
    spheres_list = response.json()
    assert any(s["id"] == sphere_id for s in spheres_list)

async def test_delete_sphere(client: AsyncClient, auth_headers: dict):
    # Create a sphere to delete
    sphere_data = {"name": "Sphere to Delete"}
    create_response = await client.post(f"{settings.API_V1_STR}/spheres/", json=sphere_data, headers=auth_headers)
    sphere_id = create_response.json()["id"]

    # Delete it
    delete_response = await client.delete(f"{settings.API_V1_STR}/spheres/{sphere_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = await client.get(f"{settings.API_V1_STR}/spheres/{sphere_id}", headers=auth_headers)
    assert get_response.status_code == 404 # Not found because it's deleted

async def test_permission_denied_sphere(client: AsyncClient, auth_headers: dict, test_user):
    # Create a sphere with user 1
    sphere_data = {"name": "User1's Private Sphere"}
    create_response = await client.post(f"{settings.API_V1_STR}/spheres/", json=sphere_data, headers=auth_headers)
    sphere_id = create_response.json()["id"]

    # Create user 2
    from tests.utils.user import create_random_user
    db = client.app.dependency_overrides[get_db_session]()
    user2 = await create_random_user(db)
    from tests.utils.user import user_authentication_headers
    user2_headers = user_authentication_headers(login=user2.login)

    # User 2 tries to access user 1's sphere
    get_response = await client.get(f"{settings.API_V1_STR}/spheres/{sphere_id}", headers=user2_headers)
    assert get_response.status_code == 403 # Forbidden