from pydantic import BaseModel


class ProductionResponse(BaseModel):
    grupo: str
    nome: str
    quantidade: float
