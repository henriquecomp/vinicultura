from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.application.DTOs.import_response import ImportResponse
from app.application.services.import_service import ImportService
from app.api.common.check_access import check_access
from app.domain.enums.import_enum import ImportEnum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/import/")
def get_import(token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023, category: ImportEnum = None) -> list[ImportResponse]:
    """
        Recupera os dados da importação de produtos de uva

        Args:
            year (int): Ano que deseja ver os dados. Caso não informado, o valor padrão será 2023.        
            category (ImportEnum): Categoria da uva, o valor padrão será em "" e trará todas as categorias.

        Returns:
            list: Uma lista seguindo a estrutura:
                [
                    {
                        "category": str, # categoria do produto
                        "country": str, # País de Importação
                        "quantity": int, # Quantidade exportada em KG
                        "value": float, # Valor total da importação em US$ (Dólar)
                    }
                ]

        Raises:
            HTTPException: Se o usuário ou senha forem inválidos.
    """    
    check_access(token)
    return ImportService().get_import(year, category)
