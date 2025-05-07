from domain.repositories.import_repository import ImportRepository
from use_cases.commands.create_import import CreateImportsCommand
from domain.entities.import_ import Import


class CreateImportsHandler:
    def __init__(self, repository: ImportRepository):
        self.repository = repository

    def handle(self, command: CreateImportsCommand):
        for item in command.items:
            import_entity = Import(
                grupo=item.grupo,
                nome=item.nome,
                quantidade=item.quantidade,
            )
            self.repository.save(import_entity)
