from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.application.DTOs.processing_response import ProcessingResponse
from app.application.services.processing_service import ProcessingService
from app.api.common.check_access import check_access
from app.domain.enums.processing_enum import ProcessingEnum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/processing/", response_model=list[ProcessingResponse])
def get_processing(token: Annotated[str, Depends(oauth2_scheme)], year: int = 2023, category: ProcessingEnum = None) -> list[ProcessingResponse]:
    """
        Recupera os dados de processamento de produtos de uva

        Args:
            year (int): Ano que deseja ver os dados. Caso não informado, o valor padrão será 2023.        
            category (ProcessingEnum): Categoria da uva, o valor padrão será em "" e trará a categoria VINIFERAS.

        Returns:
            list: Uma lista seguindo a estrutura:
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # Nome do produto
                        "quantity": int, # Quantidade processada em KG
                    }
                ]

        Raises:
            HTTPException: Se o usuário ou senha forem inválidos.
    """    
    try: 
        check_access(token)
        processing_service = ProcessingService()    
        return processing_service.get_processing(year, category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e