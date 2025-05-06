from pydantic import BaseModel


class ImportResponse(BaseModel):
    grupo: str
    pais: str
    quantidade: float
    valor: float
