from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, get_db_session
from app.crud.user import user as user_crud
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_in: UserCreate,
):
    """
    Create new user.
    """
    user = await user_crud.get_by_login(db, login=user_in.login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this login already exists in the system.",
        )
    user = await user_crud.create(db, obj_in=user_in)
    return user

@router.get("/me", response_model=UserRead)
async def read_user_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user.
    """
    return current_user