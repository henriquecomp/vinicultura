from fastapi import APIRouter
from application.DTOs.processing_response import ProcessingResponse
from application.services.processing_service import ProcessingService

router = APIRouter()


@router.post("/processing", response_model=list[ProcessingResponse])
def create_production() -> list[ProcessingResponse]:
    """
    This endpoint is not implemented yet.
    """
    pass


@router.get("/processing/", response_model=list[ProcessingResponse])
def get_processing(year: int = 2023) -> list[ProcessingResponse]:
    processing_service = ProcessingService()
    return processing_service.get_processing_by_year(year)
