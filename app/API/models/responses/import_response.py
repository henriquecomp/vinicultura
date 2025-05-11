from dataclasses import dataclass


@dataclass()
class ImportResponse:
    category: str
    country: str
    quantity: float
    value: float
