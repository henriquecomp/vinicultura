from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from application.DTOs.processing_response import ProcessingResponse
from application.services.processing_service import ProcessingService
from API.common.check_access import check_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/processing/", response_model=list[ProcessingResponse])
def get_processing(token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023) -> list[ProcessingResponse]:
    check_access(token)
    processing_service = ProcessingService()
    return processing_service.get_processing_by_year(year)
