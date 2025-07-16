from typing import Any
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Sphere, User
from app.schemas.sphere import SphereCreate, SphereUpdate

class CRUDSphere(CRUDBase[Sphere, SphereCreate]):
    async def get_multi_for_user(self, db: AsyncSession, *, user_id: int) -> list[Sphere]:
        """
        Get all spheres a user has access to (owner, reader, or editor).
        """
        query = (
            select(self.model)
            .options(selectinload(self.model.owner))
            .where(
                or_(
                    self.model.user_id == user_id,
                    self.model.readers.any(User.id == user_id),
                    self.model.editors.any(User.id == user_id)
                )
            )
            .order_by(self.model.name)
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: SphereCreate, owner_id: int
    ) -> Sphere:
        # Fetch users for relationships
        readers = []
        if obj_in.reader_ids:
            result = await db.execute(select(User).where(User.id.in_(obj_in.reader_ids)))
            readers = result.scalars().all()

        editors = []
        if obj_in.editor_ids:
            result = await db.execute(select(User).where(User.id.in_(obj_in.editor_ids)))
            editors = result.scalars().all()
        
        db_obj = self.model(
            name=obj_in.name,
            description=obj_in.description,
            user_id=owner_id,
            readers=readers,
            editors=editors,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj, ["owner"])
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Sphere, obj_in: SphereUpdate
    ) -> Sphere:
        update_data = obj_in.model_dump(exclude_unset=True)

        # Handle relationships separately
        if "reader_ids" in update_data:
            reader_ids = update_data.pop("reader_ids")
            if reader_ids is not None:
                result = await db.execute(select(User).where(User.id.in_(reader_ids)))
                db_obj.readers = result.scalars().all()

        if "editor_ids" in update_data:
            editor_ids = update_data.pop("editor_ids")
            if editor_ids is not None:
                result = await db.execute(select(User).where(User.id.in_(editor_ids)))
                db_obj.editors = result.scalars().all()
        
        # Update scalar fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj, ["owner"])
        return db_obj

sphere = CRUDSphere(Sphere)