from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, get_db_session, get_location_with_read_permission, get_location_with_edit_permission
from app.crud.location import location as location_crud
from app.models import User, Location
from app.schemas.location import LocationCreate, LocationRead, LocationUpdate

router = APIRouter()

@router.get("/", response_model=list[LocationRead])
async def read_locations(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all locations the user has access to.
    """
    locations = await location_crud.get_multi_for_user(db, user_id=current_user.id)
    return locations

@router.post("/", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
async def create_location(
    *,
    db: AsyncSession = Depends(get_db_session),
    location_in: LocationCreate,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new location.
    """
    location = await location_crud.create_with_owner(db, obj_in=location_in, owner_id=current_user.id)
    return location

@router.get("/{location_id}", response_model=LocationRead)
async def read_location(
    *,
    location: Location = Depends(get_location_with_read_permission)
):
    """
    Get a specific location by id.
    """
    return location

@router.put("/{location_id}", response_model=LocationRead)
async def update_location(
    *,
    db: AsyncSession = Depends(get_db_session),
    location_in: LocationUpdate,
    location_to_update: Location = Depends(get_location_with_edit_permission)
):
    """
    Update a location.
    """
    updated_location = await location_crud.update(db, db_obj=location_to_update, obj_in=location_in)
    return updated_location

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    *,
    db: AsyncSession = Depends(get_db_session),
    location_to_delete: Location = Depends(get_location_with_edit_permission)
):
    """
    Delete a location.
    """
    await location_crud.remove(db, id=location_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)