from dataclasses import dataclass


@dataclass()
class ProductionResponse:
    category: str
    name: str
    quantity: float
    source: str = None
