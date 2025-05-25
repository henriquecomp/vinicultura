from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.application.DTOs.commercialization_response import CommercializationResponse
from app.application.services.commercialization_service import CommercializationService
from app.api.common.check_access import check_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/commercialization/")
def get_commercialization(
    token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023
) -> list[CommercializationResponse]:
    """
    Recupera os dados da comercialização de produtos de uva

    Args:
        year (int): Ano que deseja ver os dados. Caso não informado, o valor padrão será 2023.        

    Returns:
        list: Uma lista seguindo a estrutura:
            [
                {
                    "category": str, # categoria do produto
                    "name": str, # Nome do produto
                    "quantity": int, # Quantidade comercializada em litros
                }
            ]

    Raises:
        HTTPException: Se o usuário ou senha forem inválidos.
    """
    check_access(token)
    return CommercializationService().get_commercialization_by_year(year)
