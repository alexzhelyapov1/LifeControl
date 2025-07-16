from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, get_db_session, get_sphere_with_read_permission, get_sphere_with_edit_permission
from app.crud.sphere import sphere as sphere_crud
from app.models import User, Sphere
from app.schemas.sphere import SphereCreate, SphereRead, SphereUpdate

router = APIRouter()

@router.get("/", response_model=list[SphereRead])
async def read_spheres(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all spheres the user has access to.
    """
    spheres = await sphere_crud.get_multi_for_user(db, user_id=current_user.id)
    return spheres

@router.post("/", response_model=SphereRead, status_code=status.HTTP_201_CREATED)
async def create_sphere(
    *,
    db: AsyncSession = Depends(get_db_session),
    sphere_in: SphereCreate,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new sphere.
    """
    sphere = await sphere_crud.create_with_owner(db, obj_in=sphere_in, owner_id=current_user.id)
    return sphere

@router.get("/{sphere_id}", response_model=SphereRead)
async def read_sphere(
    *,
    sphere: Sphere = Depends(get_sphere_with_read_permission)
):
    """
    Get a specific sphere by id.
    """
    return sphere

@router.put("/{sphere_id}", response_model=SphereRead)
async def update_sphere(
    *,
    db: AsyncSession = Depends(get_db_session),
    sphere_in: SphereUpdate,
    sphere_to_update: Sphere = Depends(get_sphere_with_edit_permission)
):
    """
    Update a sphere.
    """
    updated_sphere = await sphere_crud.update(db, db_obj=sphere_to_update, obj_in=sphere_in)
    return updated_sphere

@router.delete("/{sphere_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sphere(
    *,
    db: AsyncSession = Depends(get_db_session),
    sphere_to_delete: Sphere = Depends(get_sphere_with_edit_permission)
):
    """
    Delete a sphere.
    """
    await sphere_crud.remove(db, id=sphere_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)