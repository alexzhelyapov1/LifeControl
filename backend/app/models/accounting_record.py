import enum
from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class OperationType(enum.Enum):
    INCOME = "Income"
    SPEND = "Spend"

class AccountingRecord(Base):
    accounting_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    operation_type = Column(Enum(OperationType), nullable=False)
    is_transfer = Column(Boolean, default=False, nullable=False)

    sphere_id = Column(Integer, ForeignKey('spheres.id', ondelete='SET NULL'), nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id', ondelete='SET NULL'), nullable=False)
    
    sum = Column(Numeric(12, 2), nullable=False)
    description = Column(String(255), nullable=True)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    owner = relationship("User", back_populates="records")
    sphere = relationship("Sphere")
    location = relationship("Location")