from pydantic import BaseModel


class ExportResponse(BaseModel):
    grupo: str
    pais: str
    quantidade: float
    valor: float
