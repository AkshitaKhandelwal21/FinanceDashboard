from fastapi import APIRouter, Depends
from config.db import get_session
from config import db
from schemas import userSchema
from models.userModel import Registration
from sqlmodel import Session

userRouter = APIRouter()

@userRouter.post('/register')
def create_user(user: userSchema.CreateUser, session: Session = Depends(get_session)):
    try:
        response = Registration(**user.model_dump())
        session.add(response)
        session.commit()
        session.refresh(response) 
        return ("userId", response.id)
    except Exception as e:
        print(f"Error: {e}")


@userRouter.post('/details')
def add_details(detail: userSchema.AddDetails, session: Session = Depends(get_session)):
    try:
        user = session.get(Registration, detail.id)
        print(user)
        user.role = detail.role
        user.goal = detail.goal
        user.income = detail.income
        user.savings = detail.savings
        session.add(user)
        session.commit()
        session.refresh(user)
        return ("User", user)
    except Exception as e:
        print(f"Error: {e}")
