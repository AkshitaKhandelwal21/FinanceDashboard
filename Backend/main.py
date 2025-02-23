from fastapi import FastAPI

app = FastAPI()



from routes.home import router1
from routes.register import userRouter
app.include_router(router1)
app.include_router(userRouter)
