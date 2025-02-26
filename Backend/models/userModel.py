from pydantic import BaseModel, EmailStr
from datetime import date
from sqlmodel import SQLModel, Field
from typing import Optional

class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    phone: str
    dob: date
    role: Optional[str] = None
    income: Optional[float] = None
    goal: Optional[str] = None
    savings: Optional[float] = None
    password: str
    confirm_password: str
