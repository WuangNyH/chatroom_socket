from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from core.Database import Base
from core.Enum import Role


class Participants(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code_room = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)
