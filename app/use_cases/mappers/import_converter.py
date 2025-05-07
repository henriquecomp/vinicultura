from interfaces.schemas.responses.import_response import ImportResponse
from use_cases.commands.create_import import (
    CreateImportsCommand,
    CreateImportsCommandItem,
)


def create_imports_command(imports: list[ImportResponse]) -> CreateImportsCommand:
    items = [
        CreateImportsCommandItem(
            grupo=imp.grupo, nome=imp.nome, quantidade=imp.quantidade
        )
        for imp in imports
    ]
    return CreateImportsCommand(items=items)
