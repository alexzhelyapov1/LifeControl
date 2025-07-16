from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

sphere_readers_association = Table(
    'sphere_readers_association', Base.metadata,
    Column('sphere_id', Integer, ForeignKey('spheres.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

sphere_editors_association = Table(
    'sphere_editors_association', Base.metadata,
    Column('sphere_id', Integer, ForeignKey('spheres.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Sphere(Base):
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="spheres")

    readers = relationship("User", secondary=sphere_readers_association)
    editors = relationship("User", secondary=sphere_editors_association)