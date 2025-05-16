from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from application.DTOs.import_response import ImportResponse
from application.services.import_service import ImportService
from API.common.check_access import check_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/import/")
def get_import(token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023) -> list[ImportResponse]:
    check_access(token)
    return ImportService().get_import_by_year(year)
