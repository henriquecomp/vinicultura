from pydantic import BaseModel


class ProcessingResponse(BaseModel):
    grupo: str
    nome: str
    quantidade: float
