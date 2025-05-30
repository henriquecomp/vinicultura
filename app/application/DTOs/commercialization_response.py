from dataclasses import dataclass


@dataclass()
class CommercializationResponse:
    category: str
    name: str
    quantity: float
    source: str = None