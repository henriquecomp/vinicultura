from fastapi import APIRouter
from application.DTOs.production_response import ProductionResponse
from application.services.production_service import ProductionService


router = APIRouter()


@router.post("/production", response_model=list[ProductionResponse])
def create_production() -> list[ProductionResponse]:
    pass


@router.get("/production/")
def get_production(year: int = 2023):
    service = ProductionService()
    return service.get_production_by_year(year)
