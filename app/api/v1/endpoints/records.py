from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, get_db_session
from app.crud.accounting_record import record as record_crud
from app.crud.sphere import sphere as sphere_crud
from app.crud.location import location as location_crud
from app.models import User
from app.schemas.accounting_record import RecordCreate, RecordRead, PaginatedRecordRead

router = APIRouter()

async def _validate_resource_permissions(db: AsyncSession, user: User, sphere_ids: list[int] = [], location_ids: list[int] = []):
    """
    Helper to check if a user has EDIT permissions on all provided spheres and locations.
    """
    for sphere_id in set(sphere_ids):
        sphere = await sphere_crud.get(db, id=sphere_id)
        if not sphere:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sphere with id {sphere_id} not found.")
        if user.id != sphere.user_id and not any(editor.id == user.id for editor in sphere.editors) and not user.is_admin:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"You don't have edit permissions for sphere '{sphere.name}'.")
    
    for location_id in set(location_ids):
        location = await location_crud.get(db, id=location_id)
        if not location:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Location with id {location_id} not found.")
        if user.id != location.user_id and not any(editor.id == user.id for editor in location.editors) and not user.is_admin:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"You don't have edit permissions for location '{location.name}'.")


@router.get("/", response_model=PaginatedRecordRead)
async def read_records(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
):
    """
    Retrieve paginated financial records for the current user.
    """
    paginated_records = await record_crud.get_multi_for_user_paginated(
        db, user_id=current_user.id, page=page, size=size
    )
    return paginated_records


@router.post("/", response_model=list[RecordRead], status_code=status.HTTP_201_CREATED)
async def create_record(
    *,
    db: AsyncSession = Depends(get_db_session),
    record_in: RecordCreate,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new financial record.
    - **type: "Income"**: Creates a single income record.
    - **type: "Spend"**: Creates a single spend record.
    - **type: "Transfer"**: Creates a pair of records (spend + income) to represent a transfer.
    """
    spheres_to_check = []
    locations_to_check = []

    if record_in.type in ["Income", "Spend"]:
        spheres_to_check.append(record_in.sphere_id)
        locations_to_check.append(record_in.location_id)
    elif record_in.type == "Transfer":
        if record_in.transfer_type == "location":
            spheres_to_check.append(record_in.sphere_id)
            locations_to_check.extend([record_in.from_location_id, record_in.to_location_id])
        elif record_in.transfer_type == "sphere":
            spheres_to_check.extend([record_in.from_sphere_id, record_in.to_sphere_id])
            locations_to_check.append(record_in.location_id)

    await _validate_resource_permissions(db, current_user, sphere_ids=spheres_to_check, location_ids=locations_to_check)
    
    created_records = await record_crud.create_record(db, obj_in=record_in, owner_id=current_user.id)
    return created_records