from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

sphere_readers_association = Table(
    'sphere_readers_association', Base.metadata,
    Column('sphere_id', Integer, ForeignKey('sphere.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

sphere_editors_association = Table(
    'sphere_editors_association', Base.metadata,
    Column('sphere_id', Integer, ForeignKey('sphere.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class Sphere(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    owner = relationship("User", back_populates="spheres")

    readers = relationship("User", secondary=sphere_readers_association)
    editors = relationship("User", secondary=sphere_editors_association)