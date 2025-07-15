from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_admin_user, get_db_session
from app.crud.user import user as user_crud
from app.models import User
from app.schemas.user import UserRead

router = APIRouter()

@router.get("/users", response_model=list[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_db_session),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Retrieve all users. (Admin only)
    """
    users = await user_crud.get_all(db)
    return users