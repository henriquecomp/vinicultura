from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from application.DTOs.export_response import ExportResponse
from application.services.export_service import ExportService
from API.common.check_access import check_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/export/")
def get_export(
    token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023
) -> list[ExportResponse]:
    """
    Get export data for a specific year.
    Args:
        year (int): The year for which to retrieve export data. Defaults to 2023.
    Returns:
        list[ExportResponse]: A list of export data for the specified year.
    """
    check_access(token)
    return ExportService().get_export_by_year(year)
