from fastapi import APIRouter, Depends
from config.db import get_session
from config import db
from schemas import userSchema, incomeSchema
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


# @userRouter.patch('/user')
# def update_income(detail: userSchema.UpdateUser, session: Session = Depends(get_session)):
#     try:
#         user = session.get(Registration, detail.id)
#         print(user)
#         user.income = detail.income
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         return ("User", user)
#     except Exception as e:
#         print(f"Error: {e}")

@userRouter.get('/user')
def get_user(user= userSchema.ReadUser, session: Session = Depends(get_session)):
    try:
        User = session.get(Registration, user.id)
        print(User)
        users = session.get(User.model_dump())
        print(users)
        return ("User", users)
    except Exception as e:
        print("Error:", e)