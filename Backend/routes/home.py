from fastapi import APIRouter

router1 = APIRouter()

@router1.get('/')
def home_route():
    return "Hello"