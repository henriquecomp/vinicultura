from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.application.services.production_service import ProductionService
from app.api.common.check_access import check_access


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/production/")
def get_production(token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023):
    """
        Recupera os dados de produção de produtos de uva

        Args:
            year (int): Ano que deseja ver os dados. Caso não informado, o valor padrão será 2023.        

        Returns:
            list: Uma lista seguindo a estrutura:
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # Nome do produto
                        "quantity": int, # Quantidade de produção em litros
                    }
                ]

        Raises:
            HTTPException: Se o usuário ou senha forem inválidos.
    """     
    check_access(token)
    service = ProductionService()
    return service.get_production_by_year(year)
