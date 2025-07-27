import math
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, or_
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import AccountingRecord, User, Sphere, Location
from app.models.accounting_record import OperationType
from app.schemas.accounting_record import RecordCreate, RecordCreateIncome, RecordCreateSpend, RecordCreateTransfer

class CRUDAccountingRecord(CRUDBase[AccountingRecord, RecordCreate]):
    
    async def get_next_accounting_id(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.max(self.model.accounting_id)))
        max_id = result.scalar_one_or_none()
        return (max_id or 0) + 1

    async def get_multi_for_user_paginated(
        self, db: AsyncSession, *, user_id: int, page: int = 1, size: int = 20
    ) -> dict:
        """
        Get paginated records for a user.
        """
        if page < 1: page = 1
        if size < 1: size = 1

        # Query for total count
        count_query = select(func.count(self.model.id)).where(self.model.owner_id == user_id)
        total_count = (await db.execute(count_query)).scalar_one()

        # Query for items
        offset = (page - 1) * size
        query = (
            select(self.model)
            .where(self.model.owner_id == user_id)
            .options(
                selectinload(self.model.sphere).selectinload(Sphere.owner), 
                selectinload(self.model.location).selectinload(Location.owner)
            )
            .order_by(self.model.date.desc(), self.model.id.desc())
            .offset(offset)
            .limit(size)
        )
        result = await db.execute(query)
        items = result.scalars().all()

        return {
            "total": total_count,
            "page": page,
            "size": size,
            "pages": math.ceil(total_count / size) if total_count > 0 else 0,
            "items": items
        }

    async def create_record(
        self, db: AsyncSession, *, obj_in: RecordCreate, owner_id: int
    ) -> list[AccountingRecord]:
        
        acc_id = await self.get_next_accounting_id(db)
        created_records = []

        if isinstance(obj_in, (RecordCreateIncome, RecordCreateSpend)):
            op_type = OperationType.INCOME if isinstance(obj_in, RecordCreateIncome) else OperationType.SPEND
            record = self.model(
                accounting_id=acc_id,
                owner_id=owner_id,
                operation_type=op_type,
                sum=obj_in.sum,
                location_id=obj_in.location_id,
                sphere_id=obj_in.sphere_id,
                is_transfer=False
            )
            created_records.append(record)
        
        elif isinstance(obj_in, RecordCreateTransfer):
            common_data = {"accounting_id": acc_id, "owner_id": owner_id, "is_transfer": True}
            if obj_in.description: common_data["description"] = obj_in.description
            if obj_in.date: common_data["date"] = obj_in.date

            if obj_in.transfer_type == 'location':
                spend_rec = self.model(
                    **common_data,
                    operation_type=OperationType.SPEND,
                    sum=obj_in.sum,
                    location_id=obj_in.from_location_id,
                    sphere_id=obj_in.sphere_id
                )
                income_rec = self.model(
                    **common_data,
                    operation_type=OperationType.INCOME,
                    sum=obj_in.sum,
                    location_id=obj_in.to_location_id,
                    sphere_id=obj_in.sphere_id
                )
                created_records.extend([spend_rec, income_rec])
            
            elif obj_in.transfer_type == 'sphere':
                spend_rec = self.model(
                    **common_data,
                    operation_type=OperationType.SPEND,
                    sum=obj_in.sum,
                    location_id=obj_in.location_id,
                    sphere_id=obj_in.from_sphere_id
                )
                income_rec = self.model(
                    **common_data,
                    operation_type=OperationType.INCOME,
                    sum=obj_in.sum,
                    location_id=obj_in.location_id,
                    sphere_id=obj_in.to_sphere_id
                )
                created_records.extend([spend_rec, income_rec])

        if not created_records:
            return [] # Should not happen if validation passes

        db.add_all(created_records)
        await db.commit()
        for rec in created_records:
            await db.refresh(rec, ["sphere", "location"])
        return created_records

    async def remove_by_accounting_id(self, db: AsyncSession, *, accounting_id: int, user_id: int) -> int:
        """ Deletes all records for a given accounting_id and user_id. Returns number of deleted rows. """
        query = self.model.__table__.delete().where(
            self.model.accounting_id == accounting_id,
            self.model.owner_id == user_id
        )
        result = await db.execute(query)
        await db.commit()
        return result.rowcount

    async def update_record(
        self, db: AsyncSession, *, db_obj: AccountingRecord, obj_in: RecordCreate
    ) -> AccountingRecord:
        """
        Update a single record. For transfers, this will update both related records.
        """
        if isinstance(obj_in, (RecordCreateIncome, RecordCreateSpend)):
            # Update single record
            db_obj.operation_type = OperationType.INCOME if isinstance(obj_in, RecordCreateIncome) else OperationType.SPEND
            db_obj.sum = obj_in.sum
            db_obj.location_id = obj_in.location_id
            db_obj.sphere_id = obj_in.sphere_id
            if hasattr(obj_in, 'description'):
                db_obj.description = obj_in.description
            if hasattr(obj_in, 'date'):
                db_obj.date = obj_in.date
            
            await db.commit()
            await db.refresh(db_obj, ["sphere", "location", "sphere.owner", "location.owner"])
            return db_obj
        
        elif isinstance(obj_in, RecordCreateTransfer):
            # For transfers, we need to update both records with the same accounting_id
            # First, delete existing records for this accounting_id
            await self.remove_by_accounting_id(db, accounting_id=db_obj.accounting_id, user_id=db_obj.owner_id)
            
            # Then create new records
            return (await self.create_record(db, obj_in=obj_in, owner_id=db_obj.owner_id))[0]
        
        return db_obj

record = CRUDAccountingRecord(AccountingRecord)