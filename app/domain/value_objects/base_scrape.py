from dataclasses import dataclass


@dataclass()
class BaseScrapeValueObject:
    category: str
    name: str
    quantity: float
    value: float
