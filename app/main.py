from fastapi import FastAPI
from interfaces.controllers.user_controller import router as user_controller
from interfaces.controllers.production_controller import router as production_controller


app = FastAPI()

app.include_router(user_controller)
app.include_router(production_controller)
