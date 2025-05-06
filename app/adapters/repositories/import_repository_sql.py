from domain.repositories.import_repository import ImportRepository
from interfaces.schemas.responses.import_response import ImportResponse


class ImportRepositorySQL(ImportRepository):
    def save(self, items: list[ImportResponse]) -> list[ImportResponse]:
        # Implement the logic to save items to the database
        pass
