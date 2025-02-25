from fastapi import APIRouter
from models.userModel import Registration

userRouter = APIRouter()

@userRouter.post('/register')
def register(user: Registration):
    return {"user": user}
    