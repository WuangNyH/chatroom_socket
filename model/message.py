from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from core.Database import Base
from core.Enum import Role


class Message(Base):
    __tablename__ = 'messengers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code_room = Column(Integer, nullable=False)
    content = Column(String(500), nullable=False)
    name = Column(String(255), nullable=False)
