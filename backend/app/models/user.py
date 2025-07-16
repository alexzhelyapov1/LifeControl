from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# Association table for friends (many-to-many self-referencing)
user_friends_association = Table(
    'user_friends_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    login = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    description = Column(String(255), nullable=True)
    is_admin = Column(Boolean(), default=False)
    
    friends = relationship(
        "User",
        secondary=user_friends_association,
        primaryjoin=id == user_friends_association.c.user_id,
        secondaryjoin=id == user_friends_association.c.friend_id,
        backref="friend_of"
    )
    
    # Relationships to owned items
    spheres = relationship("Sphere", back_populates="owner", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="owner", cascade="all, delete-orphan")
    records = relationship("AccountingRecord", back_populates="owner", cascade="all, delete-orphan")