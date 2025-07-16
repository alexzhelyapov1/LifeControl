import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user as user_crud
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import create_access_token

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_login() -> str:
    return f"user_{random_lower_string()[:8]}"

async def create_random_user(db: AsyncSession, is_admin: bool = False) -> User:
    login = random_login()
    password = random_lower_string()
    user_in = UserCreate(login=login, password=password)
    user = await user_crud.create(db, obj_in=user_in)
    if is_admin:
        user.is_admin = True
        await db.commit()
        await db.refresh(user)
    return user

def user_authentication_headers(
    *, login: str, password: str = "password"
) -> dict[str, str]:
    # Note: In a real scenario, you'd get the token from the /token endpoint.
    # For testing, we create it directly to simplify.
    # To do this "properly", you'd need the client fixture to make a request.
    # This is a common shortcut in tests.
    access_token = create_access_token(login)
    return {"Authorization": f"Bearer {access_token}"}