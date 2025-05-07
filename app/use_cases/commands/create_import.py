from dataclasses import dataclass
from typing import List


@dataclass
class CreateImportsCommandItem:
    grupo: str
    nome: str
    quantidade: float


@dataclass
class CreateImportsCommand:
    items: List[CreateImportsCommandItem]
