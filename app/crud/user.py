from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class CRUDUser(CRUDBase[User, UserCreate]):
    async def get_by_login(self, db: AsyncSession, *, login: str) -> User | None:
        result = await db.execute(select(self.model).filter(self.model.login == login))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = self.model(
            login=obj_in.login,
            hashed_password=get_password_hash(obj_in.password),
            description=obj_in.description,
            is_admin=False  # Users cannot register as admins
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

user = CRUDUser(User)