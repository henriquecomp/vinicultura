from fastapi import FastAPI
from API.controllers.auth_controller import router as auth_controller
from API.controllers.production_controller import router as production_controller
from API.controllers.processing_controller import router as processing_controller
from API.controllers.commercialization_controller import router as commercialization_controller
from API.controllers.import_controller import router as import_controller
from API.controllers.export_controller import router as export_controller
from API.controllers.user_controller import router as user_controller


app = FastAPI()

app.include_router(auth_controller)
app.include_router(production_controller)
app.include_router(processing_controller)
app.include_router(commercialization_controller)
app.include_router(import_controller)
app.include_router(export_controller)
app.include_router(user_controller)
