from sqlmodel import create_engine, Session, select
from sqlmodel import SQLModel
from models.userModel import Registration
from typing import Annotated
from fastapi import Depends

DATABASE_URI = "mysql+mysqldb://root:AKSHITA@localhost/user"

engine = create_engine(DATABASE_URI)
SQLModel.metadata.create_all(engine)
session = Session(engine)
