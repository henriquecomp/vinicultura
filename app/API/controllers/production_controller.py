from fastapi import APIRouter
from application.services.production_service import ProductionService


router = APIRouter()


@router.get("/production/")
def get_production(year: int = 2023):
    service = ProductionService()
    return service.get_production_by_year(year)
