from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from application.DTOs.commercialization_response import CommercializationResponse
from application.services.commercialization_service import CommercializationService
from API.common.check_access import check_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/commercialization/")
def get_comercialization(token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023) -> list[CommercializationResponse]:
    check_access(token)
    return CommercializationService().get_commercialization_by_year(year)
