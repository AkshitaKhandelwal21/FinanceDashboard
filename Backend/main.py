from fastapi import FastAPI
from sqlmodel import SQLModel
from config.db import create_db_and_tables

app = FastAPI()

create_db_and_tables()

from routes.home import router1
from routes.register import userRouter
app.include_router(router1)
app.include_router(userRouter)
