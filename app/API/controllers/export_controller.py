from fastapi import APIRouter
from application.DTOs.export_response import ExportResponse
from application.services.export_service import ExportService

router = APIRouter()


@router.get("/export/")
def get_export(year: int = 2023) -> list[ExportResponse]:
    """
    Get export data for a specific year.
    Args:
        year (int): The year for which to retrieve export data. Defaults to 2023.
    Returns:
        list[ExportResponse]: A list of export data for the specified year.
    """
    return ExportService().get_export_by_year(year)
