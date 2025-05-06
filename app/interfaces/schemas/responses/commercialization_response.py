from pydantic import BaseModel


class CommercializationResponse(BaseModel):
    grupo: str
    nome: str
    quantidade: float
