from fastapi import APIRouter
from application.DTOs.commercialization_response import CommercializationResponse
from application.services.commercialization_service import CommercializationService

router = APIRouter()


@router.post("/commercialization", response_model=list[CommercializationResponse])
def create_comercialization() -> list[CommercializationResponse]:
    pass


@router.get("/commercialization/")
def get_comercialization(year: int = 2023) -> list[CommercializationResponse]:
    return CommercializationService().get_commercialization_by_year(year)
