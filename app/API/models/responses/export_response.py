from pydantic import BaseModel


class ExportResponse(BaseModel):
    category: str
    country: str
    quantity: float
    value: float
