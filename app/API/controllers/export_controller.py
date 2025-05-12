from fastapi import APIRouter
from application.DTOs.export_response import ExportResponse
from application.services.export_service import ExportService

router = APIRouter()


@router.post("/export", response_model=list[ExportResponse])
def create_import() -> list[ExportResponse]:
    pass


@router.get("/export/")
def get_export(year: int = 2023) -> list[ExportResponse]:
    return ExportService().get_export_by_year(year)
