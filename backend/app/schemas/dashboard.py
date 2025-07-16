from pydantic import BaseModel

class BalanceItem(BaseModel):
    id: int
    name: str
    balance: float

class DashboardData(BaseModel):
    total_balance: float
    locations_balance: list[BalanceItem]
    spheres_balance: list[BalanceItem] # Income - Spend