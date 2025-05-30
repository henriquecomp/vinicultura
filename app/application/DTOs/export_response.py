from dataclasses import dataclass


@dataclass()
class ExportResponse():
    category: str
    country: str
    quantity: float
    value: float
    source: str = None
