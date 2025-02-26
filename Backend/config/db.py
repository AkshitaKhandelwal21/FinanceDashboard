from sqlmodel import create_engine, Session, select
from sqlmodel import SQLModel
from models.userModel import Registration
from fastapi import Depends
from typing import Annotated


DATABASE_URI = "mysql+mysqldb://root:AKSHITA@localhost/user"

engine = create_engine(DATABASE_URI)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  

def get_session():
    with Session(engine) as session:
        yield session

print("Moving to main file")
