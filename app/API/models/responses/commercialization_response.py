from pydantic import BaseModel


class CommercializationResponse(BaseModel):
    category: str
    name: str
    quantity: float
