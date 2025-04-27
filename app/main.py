from fastapi import FastAPI
from interfaces.controllers.user_controller import router as user_controller


app = FastAPI()

app.include_router(user_controller)
