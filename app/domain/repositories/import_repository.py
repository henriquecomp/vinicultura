from interfaces.schemas.responses.import_response import ImportResponse
from abc import ABC, abstractmethod


class ImportRepository(ABC):
    @abstractmethod
    def save(self, items: list[ImportResponse]) -> None:
        pass
