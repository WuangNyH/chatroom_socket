from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AccountSchema(BaseModel):
    full_name: str
    email: EmailStr
    nickname: str
    password: str


class AccountLogin(BaseModel):
    email: EmailStr
    password: str
