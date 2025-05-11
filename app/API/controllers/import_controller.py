from fastapi import APIRouter
from API.models.responses.import_response import ImportResponse
from application.services.import_service import ImportService

router = APIRouter()


@router.post("/import", response_model=list[ImportResponse])
def create_import() -> list[ImportResponse]:
    pass


@router.get("/import/")
def get_import(year: int = 2023) -> list[ImportResponse]:
    return ImportService().get_import_by_year(year)
