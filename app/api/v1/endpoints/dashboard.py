from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, get_db_session
from app.crud.dashboard import dashboard as dashboard_crud
from app.models import User
from app.schemas.dashboard import DashboardData

router = APIRouter()

@router.get("/", response_model=DashboardData)
async def read_dashboard_data(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get aggregated dashboard data for the current user.
    If an admin uses `as_user_id` query param, the data will be for that user.
    """
    data = await dashboard_crud.get_dashboard_data(db, user_id=current_user.id)
    return data