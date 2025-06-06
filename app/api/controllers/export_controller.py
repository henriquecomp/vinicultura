from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.application.DTOs.export_response import ExportResponse
from app.application.services.export_service import ExportService
from app.api.common.check_access import check_access
from app.domain.enums.export_enum import ExportEnum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/export/")
def get_export(
    token: Annotated[str, Depends(oauth2_scheme)],
    year: int = 2024,
    category: ExportEnum = None,
) -> list[ExportResponse]:
    """
    Recupera os dados da exportação de produtos de uva

    Args:
        year (int): Ano que deseja ver os dados. Caso não informado, o valor padrão será 2024.
        category (ExportEnum): Categoria da uva, o valor padrão será em "" e trará a categoria Vinho de mesa


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
    try: 
        check_access(token)
        exportService = ExportService()
        return exportService.get_export(year, category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e