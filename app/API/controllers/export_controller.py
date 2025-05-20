from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from application.DTOs.export_response import ExportResponse
from application.services.export_service import ExportService
from api.common.check_access import check_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/export/")
def get_export(
    token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023
) -> list[ExportResponse]:
    """
        Recupera os dados da exportação de produtos de uva

        Args:
            year (int): Ano que deseja ver os dados. Caso não informado, o valor padrão será 2023.        

        Returns:
            list: Uma lista seguindo a estrutura:
                [
                    {
                        "category": str, # categoria do produto
                        "country": str, # País de exportação
                        "quantity": int, # Quantidade exportada em KG
                        "value": float, # Valor total da exportação em US$ (Dólar)
                    }
                ]

        Raises:
            HTTPException: Se o usuário ou senha forem inválidos.
    """
    check_access(token)
    return ExportService().get_export_by_year(year)
