from sqlalchemy import func, select, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models import AccountingRecord, Location, Sphere
from app.models.accounting_record import OperationType
from app.schemas.dashboard import DashboardData, BalanceItem

class CRUDDashboard:
    async def get_dashboard_data(self, db: AsyncSession, *, user_id: int) -> DashboardData:
        # 1. Calculate total balance across all locations
        total_balance_query = (
            select(
                func.sum(
                    case(
                        (AccountingRecord.operation_type == OperationType.INCOME, AccountingRecord.sum),
                        (AccountingRecord.operation_type == OperationType.SPEND, -AccountingRecord.sum),
                    )
                )
            )
            .where(AccountingRecord.user_id == user_id)
        )
        total_balance_res = await db.execute(total_balance_query)
        total_balance = total_balance_res.scalar_one_or_none() or 0.0

        # 2. Calculate balance per location
        location_balance_query = (
            select(
                Location.id,
                Location.name,
                func.sum(
                    case(
                        (AccountingRecord.operation_type == OperationType.INCOME, AccountingRecord.sum),
                        (AccountingRecord.operation_type == OperationType.SPEND, -AccountingRecord.sum),
                    )
                ).label("balance")
            )
            .join(AccountingRecord, AccountingRecord.location_id == Location.id)
            .where(AccountingRecord.user_id == user_id)
            .group_by(Location.id, Location.name)
            .order_by(Location.name)
        )
        location_balances_res = await db.execute(location_balance_query)
        locations_balance = [BalanceItem(id=row.id, name=row.name, balance=float(row.balance)) for row in location_balances_res.all()]
        
        # 3. Calculate balance per sphere (Income - Spend, non-transfers)
        sphere_balance_query = (
            select(
                Sphere.id,
                Sphere.name,
                func.sum(
                     case(
                        (AccountingRecord.operation_type == OperationType.INCOME, AccountingRecord.sum),
                        (AccountingRecord.operation_type == OperationType.SPEND, -AccountingRecord.sum),
                    )
                ).label("balance")
            )
            .join(AccountingRecord, AccountingRecord.sphere_id == Sphere.id)
            .where(
                AccountingRecord.user_id == user_id,
                AccountingRecord.is_transfer == False
            )
            .group_by(Sphere.id, Sphere.name)
            .order_by(Sphere.name)
        )
        sphere_balances_res = await db.execute(sphere_balance_query)
        spheres_balance = [BalanceItem(id=row.id, name=row.name, balance=float(row.balance)) for row in sphere_balances_res.all()]

        return DashboardData(
            total_balance=float(total_balance),
            locations_balance=locations_balance,
            spheres_balance=spheres_balance
        )

dashboard = CRUDDashboard()