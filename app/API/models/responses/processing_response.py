from pydantic import BaseModel


class ProcessingResponse(BaseModel):
    category: str
    name: str
    quantity: float
