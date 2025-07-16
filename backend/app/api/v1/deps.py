from typing import AsyncGenerator, Callable
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core import security
from app.core.config import settings
from app.crud import user as user_crud
from app.crud.base import CRUDBase
from app.db.session import get_db_session
from app.models import User, Sphere, Location
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
    as_user_id: int | None = Query(None, description="Admin: ID of user to view as")
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(sub=payload.get("sub"))
    except (JWTError, ValidationError):
        raise credentials_exception
    
    if token_data.sub is None:
        raise credentials_exception
        
    # User making the request based on the token
    requesting_user = await user_crud.user.get_by_login(db, login=token_data.sub)
    if not requesting_user:
        raise credentials_exception

    # If admin wants to view as another user
    if as_user_id and requesting_user.is_admin:
        effective_user = await user_crud.user.get(db, id=as_user_id)
        if not effective_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {as_user_id} not found",
            )
        return effective_user

    # Default case: return the user from the token
    return requesting_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


# Новая фабрика зависимостей
def get_resource_with_permissions_factory(
    crud_repo: CRUDBase,
    permission_level: str  # "read" or "edit"
) -> Callable:
    async def get_resource(
        resource_id: int,
        db: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user),
    ):
        # Eager load relationships needed for permission checks
        query_options = [
            selectinload(crud_repo.model.owner),
            selectinload(crud_repo.model.readers),
            selectinload(crud_repo.model.editors),
        ]
        
        # Загружаем ресурс с предзагрузкой связей
        result = await db.execute(
            crud_repo.model.__table__.select()
            .where(crud_repo.model.id == resource_id)
            .options(*query_options)
        )
        resource = (await db.execute(
            select(crud_repo.model)
            .where(crud_repo.model.id == resource_id)
            .options(*query_options))
        ).scalars().first()


        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

        if current_user.is_admin:
            return resource

        if current_user.id == resource.user_id:
            return resource

        user_is_reader = any(reader.id == current_user.id for reader in resource.readers)
        user_is_editor = any(editor.id == current_user.id for editor in resource.editors)

        if permission_level == "read" and (user_is_reader or user_is_editor):
            return resource
        
        if permission_level == "edit" and user_is_editor:
            return resource

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return get_resource

# Создаем конкретные зависимости для использования в эндпоинтах
from app.crud.sphere import sphere as sphere_crud
from app.crud.location import location as location_crud

get_sphere_with_read_permission = get_resource_with_permissions_factory(sphere_crud, "read")
get_sphere_with_edit_permission = get_resource_with_permissions_factory(sphere_crud, "edit")
get_location_with_read_permission = get_resource_with_permissions_factory(location_crud, "read")
get_location_with_edit_permission = get_resource_with_permissions_factory(location_crud, "edit")