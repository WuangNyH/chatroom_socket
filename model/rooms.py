from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from core.Database import Base
from core.Enum import Role


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code_room = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    