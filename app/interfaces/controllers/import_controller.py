from fastapi import APIRouter
from interfaces.schemas.responses.import_response import ImportResponse
from use_cases.queries.import_scrape import ImportScrape
from use_cases.commands.create_import import CreateImportsCommand
from use_cases.handlers.create_import_handler import CreateImportsHandler

# from sqlalchemy.orm import Session
# from interfaces.schemas.requests.user_create_request import UserCreateRequest
# from interfaces.schemas.responses.user_response import UserResponse
# from use_cases.commands.create_user import CreateUserUseCase
# from use_cases.queries.get_user_by_email import GetUserByEmailQuery
# from adapters.repositories.user_repository_sql import UserRepositorySQL
# from adapters.db.database import get_db

router = APIRouter()


# def get_command_use_case(session: Session = Depends(get_db)):
#     return CreateUserUseCase(UserRepositorySQL(session))


# def get_query_use_case(session: Session = Depends(get_db)):
# return GetUserByEmailQuery(UserRepositorySQL(session))


@router.post("/import", response_model=list[ImportResponse])
def create_import() -> list[ImportResponse]:
    use_case = ImportScrape()
    data = use_case.execute()
    scrapes = CreateImportsCommand(data)
    use_case_command = CreateImportsHandler()
    use_case_command.handle(scrapes)
    return data


@router.get("/import/{name}")
def get_import():
    return {"message": "Dados recuperado com sucesso"}
