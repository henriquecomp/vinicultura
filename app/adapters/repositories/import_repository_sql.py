from sqlalchemy.orm import Session
from domain.repositories.import_repository import ImportRepository
from domain.entities.import_ import Import


class ImportRepositorySQL(ImportRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, item: Import) -> bool:
        self.session.add(item)
        self.session.commit()
        return True
