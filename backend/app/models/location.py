from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

location_readers_association = Table(
    'location_readers_association', Base.metadata,
    Column('location_id', Integer, ForeignKey('locations.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

location_editors_association = Table(
    'location_editors_association', Base.metadata,
    Column('location_id', Integer, ForeignKey('locations.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Location(Base):
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="locations")

    readers = relationship("User", secondary=location_readers_association)
    editors = relationship("User", secondary=location_editors_association)