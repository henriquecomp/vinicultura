from dataclasses import dataclass


@dataclass()
class ConfigResponse:
    category: str
    url: str
    file: str
