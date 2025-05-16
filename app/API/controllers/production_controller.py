from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from application.services.production_service import ProductionService
from API.common.check_access import check_access


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/production/")
def get_production(token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023):
    check_access(token)
    service = ProductionService()
    return service.get_production_by_year(year)
