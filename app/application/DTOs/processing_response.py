from dataclasses import dataclass


@dataclass()
class ProcessingResponse:
    category: str
    name: str
    quantity: float
    source: str = None
