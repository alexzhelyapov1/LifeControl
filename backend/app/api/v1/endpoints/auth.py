from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.crud.user import user as user_crud
from app.schemas.token import Token
from app.api.v1.deps import get_db_session

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()] = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await user_crud.get_by_login(db, login=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.login, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}