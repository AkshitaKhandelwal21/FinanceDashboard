from pydantic import BaseModel, EmailStr
from datetime import date
from sqlmodel import Field, SQLModel
from typing import Optional

class CreateUser(SQLModel):
    name: str
    email: EmailStr
    phone: str
    dob: date
    password: str
    confirm_password: str

class ReadUser(SQLModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class AddDetails(SQLModel):
    id: int
    role: str
    income: float
    goal: str
    savings: Optional[float] = Field(default=None)
