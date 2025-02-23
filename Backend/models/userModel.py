from pydantic import BaseModel, EmailStr
from datetime import date
from sqlmodel import SQLModel, Field

class Registration(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: EmailStr
    phone: int
    dob: date
    password: str
    confirm_password: str
